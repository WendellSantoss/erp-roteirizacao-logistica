"""Finalização do planejamento (HU-013) e geração do arquivo RPA (HU-014)."""

from dataclasses import dataclass

from django.db import transaction
from django.utils import timezone

from nucleo import services_preparacao
from nucleo.excecoes import RecursoNaoEncontrado
from nucleo.models import EstadoOS
from nucleo.services import Alteracao, Autoria, registrar_auditoria
from roteirizacao import arquivo_rpa, consultas
from roteirizacao.excecoes import (
    PlanejamentoFinalizado,
    PlanejamentoInconsistente,
    PlanejamentoNaoFinalizado,
)
from roteirizacao.models import ArquivoDespacho, Planejamento, StatusPlanejamento
from roteirizacao.services import ChavePlanejamento

ENTIDADE_PLANEJAMENTO = "Planejamento"


@dataclass(frozen=True)
class Inconsistencia:
    rota: str
    motivo: str


# ── Finalizar (HU-013) ────────────────────────────────────────────────────────


@transaction.atomic
def finalizar_planejamento(chave: ChavePlanejamento, usuario) -> Planejamento:
    """Fecha o planejamento se todas as rotas estão consistentes (RN-L02); senão nada muda."""
    planejamento = consultas.planejamento_existente_para_alterar(
        chave.polo_id, chave.operacao_id, chave.data
    )
    rotas = consultas.rotas_do_planejamento(planejamento.pk) if planejamento else []
    if not rotas:
        raise PlanejamentoInconsistente("Não há rotas para finalizar")  # CA04
    if planejamento.status != StatusPlanejamento.ABERTO:
        raise PlanejamentoFinalizado()
    inconsistencias = encontrar_inconsistencias(planejamento, rotas)
    if inconsistencias:
        detalhes = {"inconsistencias": [vars(item) for item in inconsistencias]}
        raise PlanejamentoInconsistente(detalhes=detalhes)  # CA02
    planejamento.status = StatusPlanejamento.FINALIZADO
    planejamento.finalizado_em = timezone.now()
    planejamento.finalizado_por = usuario
    planejamento.save(update_fields=["status", "finalizado_em", "finalizado_por"])
    _auditar_status(planejamento, StatusPlanejamento.ABERTO, Autoria(usuario, "Finalizado"))
    return planejamento


def encontrar_inconsistencias(planejamento: Planejamento, rotas) -> list[Inconsistencia]:
    """Lista cada rota com o motivo que impede a finalização (HU-013 RN-L02)."""
    inconsistencias = []
    for rota in rotas:
        inconsistencias += [
            Inconsistencia(rota.nome, m) for m in _motivos_da_rota(planejamento, rota)
        ]
    inconsistencias += _excessos_de_capacidade(planejamento, rotas)
    return inconsistencias


def _motivos_da_rota(planejamento: Planejamento, rota) -> list[str]:
    motivos = []
    itens = list(rota.itens.all())
    if not itens:
        motivos.append("Rota sem OS")
    if not rota.equipe.ativa:
        motivos.append(f"{rota.equipe.nome} foi inativada")
    if rota.equipe.polo_id != planejamento.polo_id:
        motivos.append(f"{rota.equipe.nome} não é do polo do planejamento")
    fora = [i.ordem_servico.numero for i in itens if i.ordem_servico.estado != EstadoOS.ROTEIRIZADA]
    if fora:
        motivos.append(f"OSs que não estão mais roteirizadas: {', '.join(fora)}")
    return motivos


def _excessos_de_capacidade(planejamento: Planejamento, rotas) -> list[Inconsistencia]:
    totais = consultas.ordens_por_equipe_no_dia(planejamento.polo_id, planejamento.data)
    equipes = {rota.equipe.pk: rota.equipe for rota in rotas}
    return [
        Inconsistencia(
            equipe.nome,
            f"{totais[equipe.pk]} OSs no dia excede a capacidade de {equipe.capacidade_diaria}",
        )
        for equipe in equipes.values()
        if totais.get(equipe.pk, 0) > equipe.capacidade_diaria
    ]


# ── Gerar e baixar o arquivo RPA (HU-014) ─────────────────────────────────────


@dataclass(frozen=True)
class ResultadoGeracao:
    arquivo: ArquivoDespacho
    gerado_agora: bool


@transaction.atomic
def gerar_arquivo_rpa(chave: ChavePlanejamento, usuario) -> ResultadoGeracao:
    """Gera o arquivo e despacha as OSs, tudo ou nada (RN-L03); repetir devolve o mesmo (RN-L02)."""
    planejamento = consultas.planejamento_existente_para_alterar(
        chave.polo_id, chave.operacao_id, chave.data
    )
    if planejamento is None or planejamento.status == StatusPlanejamento.ABERTO:
        raise PlanejamentoNaoFinalizado()  # CA02
    if planejamento.status == StatusPlanejamento.DESPACHADO:
        return ResultadoGeracao(consultas.arquivo_do_planejamento(planejamento.pk), False)
    rotas = consultas.rotas_do_planejamento(planejamento.pk)
    conteudo = arquivo_rpa.montar_conteudo(planejamento, rotas)
    ordens_ids = [item.ordem_servico_id for rota in rotas for item in rota.itens.all()]
    autoria = Autoria(usuario, "Despachada pelo arquivo RPA")
    services_preparacao.despachar_ordens(ordens_ids, chave.polo_id, autoria)  # RN-10
    arquivo = ArquivoDespacho.objects.create(
        planejamento=planejamento,
        nome_arquivo=arquivo_rpa.nome_do_arquivo(planejamento),
        conteudo=conteudo,
        hash_sha256=arquivo_rpa.calcular_hash(conteudo),
        total_ordens=len(ordens_ids),
        gerado_por=usuario,
    )
    planejamento.status = StatusPlanejamento.DESPACHADO
    planejamento.save(update_fields=["status"])
    _auditar_status(planejamento, StatusPlanejamento.FINALIZADO, autoria)
    return ResultadoGeracao(arquivo, True)


def arquivo_gerado(chave: ChavePlanejamento) -> ArquivoDespacho:
    """Mesmo arquivo, mesmo hash, sem mudar nenhuma OS (HU-014 CA04)."""
    planejamento = consultas.planejamento_do_dia(chave.polo_id, chave.operacao_id, chave.data)
    arquivo = consultas.arquivo_do_planejamento(planejamento.pk) if planejamento else None
    if arquivo is None:
        raise RecursoNaoEncontrado("Ainda não há arquivo RPA para este planejamento.")
    return arquivo


def _auditar_status(planejamento: Planejamento, anterior: str, autoria: Autoria) -> None:
    alteracao = Alteracao(
        ENTIDADE_PLANEJAMENTO, planejamento.pk, "status", anterior, planejamento.status
    )
    registrar_auditoria(planejamento.polo_id, alteracao, autoria)
