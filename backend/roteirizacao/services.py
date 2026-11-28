"""Planejamento do dia e criação de rotas (HU-011, HU-012, HU-056).

A seleção por polígono acontece no navegador (HU-012); o servidor recebe a lista de OSs e
revalida tudo (RN-08, RN-09), porque a regra vale no servidor (HU-020 RN-L01).
"""

from dataclasses import dataclass
from datetime import date, time

from django.db import transaction
from django.utils import timezone

from nucleo import consultas as consultas_nucleo
from nucleo import services_preparacao
from nucleo.excecoes import RecursoNaoEncontrado
from nucleo.services import Alteracao, Autoria, registrar_auditoria
from roteirizacao import consultas
from roteirizacao.excecoes import OrdemJaEmRota, PlanejamentoFinalizado, RegraDeRotaViolada
from roteirizacao.models import ItemRota, Planejamento, Rota, StatusPlanejamento

MENSAGEM_DATA_PASSADA = "Planejamento de data passada é somente leitura"
MENSAGEM_FINALIZADO = "Planejamento finalizado"


@dataclass(frozen=True)
class ChavePlanejamento:
    """HU-013 RN-L01: o planejamento é identificado por polo + operação + data."""

    polo_id: int
    operacao_id: int
    data: date


# ── Painel do Roteirizador (HU-011, HU-012) ───────────────────────────────────


@dataclass(frozen=True)
class Painel:
    operacao: object
    planejamento: Planejamento | None
    rotas: list[Rota]
    ordens_aptas: list
    motivo_somente_leitura: str

    @property
    def somente_leitura(self) -> bool:
        return bool(self.motivo_somente_leitura)


def listar_operacoes():
    """Operações ativas para o seletor do Roteirizador (HU-011 RN-L01)."""
    return consultas.operacoes_ativas()


def consultar_painel(chave: ChavePlanejamento) -> Painel:
    """OSs aptas do polo e rotas já criadas para a operação e a data escolhidas (HU-011 CA01)."""
    operacao = _operacao(chave.operacao_id)
    planejamento = consultas.planejamento_do_dia(chave.polo_id, chave.operacao_id, chave.data)
    rotas = consultas.rotas_do_planejamento(planejamento.pk) if planejamento else []
    return Painel(
        operacao=operacao,
        planejamento=planejamento,
        rotas=rotas,
        ordens_aptas=services_preparacao.ordens_aptas_no_mapa(chave.polo_id),
        motivo_somente_leitura=_motivo_somente_leitura(planejamento, chave.data),
    )


def _operacao(operacao_id: int):
    operacao = consultas.operacao_ativa(operacao_id)
    if operacao is None:
        raise RecursoNaoEncontrado("Operação não encontrada.")
    return operacao


def _motivo_somente_leitura(planejamento: Planejamento | None, data: date) -> str:
    if data < timezone.localdate():
        return MENSAGEM_DATA_PASSADA  # HU-011 CA02
    if planejamento and planejamento.status != StatusPlanejamento.ABERTO:
        return MENSAGEM_FINALIZADO  # HU-013 CA03
    return ""


# ── Criação de rota (HU-056) ──────────────────────────────────────────────────


@dataclass(frozen=True)
class PedidoRota:
    chave: ChavePlanejamento
    nome: str
    equipe_id: int
    previsao_inicio: time
    carregamento: time
    ordens_ids: list[int]
    cor: str = ""
    observacao: str = ""


def criar_rota(pedido: PedidoRota, usuario) -> Rota:
    """Cria a rota e leva as OSs a "Roteirizada" na mesma transação, com auditoria (CA07)."""
    if pedido.chave.data < timezone.localdate():
        raise RegraDeRotaViolada("A data da rota não pode ser anterior a hoje")  # RN-L04
    _operacao(pedido.chave.operacao_id)
    ordens_ids = list(dict.fromkeys(pedido.ordens_ids))
    with transaction.atomic():
        planejamento = _planejamento_aberto(pedido.chave)
        equipe = _equipe_da_rota(pedido.equipe_id, pedido.chave.polo_id)
        _garantir_fora_de_outras_rotas(ordens_ids)
        _garantir_capacidade(equipe, pedido.chave.data, len(ordens_ids))
        autoria = Autoria(usuario, f"Incluída na rota {pedido.nome}")
        services_preparacao.roteirizar_ordens(ordens_ids, pedido.chave.polo_id, autoria)
        rota = _gravar_rota(planejamento, pedido, usuario)
        _gravar_itens(rota, ordens_ids)
        _auditar_criacao(rota, ordens_ids, Autoria(usuario, "Rota criada"))
    return rota


def _planejamento_aberto(chave: ChavePlanejamento) -> Planejamento:
    planejamento = consultas.planejamento_para_alterar(chave.polo_id, chave.operacao_id, chave.data)
    if planejamento.status != StatusPlanejamento.ABERTO:
        raise PlanejamentoFinalizado()
    return planejamento


def _equipe_da_rota(equipe_id: int, polo_id: int):
    """RN-09: a equipe precisa ser do polo das OSs e estar ativa."""
    equipe = consultas_nucleo.equipe_por_id(equipe_id)
    if equipe is None:
        raise RecursoNaoEncontrado("Equipe não encontrada.")
    if equipe.polo_id != polo_id:
        raise RegraDeRotaViolada("A equipe pertence a outro polo.")
    if not equipe.ativa:
        raise RegraDeRotaViolada(f"{equipe.nome} está inativa.")
    return equipe


def _garantir_fora_de_outras_rotas(ordens_ids: list[int]) -> None:
    em_rota = consultas.rotas_das_ordens(ordens_ids)
    if em_rota:
        descricao = "; ".join(f"OS {numero} já está na rota {rota}" for numero, rota in em_rota)
        detalhes = {"ordens": [{"numero": numero, "rota": rota} for numero, rota in em_rota]}
        raise OrdemJaEmRota(descricao, detalhes)


def _garantir_capacidade(equipe, data: date, novas: int) -> None:
    """RN-L03: a soma do dia (todas as rotas) não passa da capacidade diária da equipe."""
    total = consultas.ordens_da_equipe_no_dia(equipe.pk, data) + novas
    if total > equipe.capacidade_diaria:
        raise RegraDeRotaViolada(
            f"{equipe.nome}: {total} OSs no dia excede a capacidade de {equipe.capacidade_diaria}",
            {"total_no_dia": total, "capacidade_diaria": equipe.capacidade_diaria},
        )


def _gravar_rota(planejamento: Planejamento, pedido: PedidoRota, usuario) -> Rota:
    return Rota.objects.create(
        planejamento=planejamento,
        nome=pedido.nome.strip(),
        equipe_id=pedido.equipe_id,
        previsao_inicio=pedido.previsao_inicio,
        carregamento=pedido.carregamento,
        cor=pedido.cor,
        observacao=pedido.observacao.strip(),
        criada_por=usuario,
    )


def _gravar_itens(rota: Rota, ordens_ids: list[int]) -> None:
    itens = [
        ItemRota(rota=rota, ordem_servico_id=ordem_id, sequencia=posicao)
        for posicao, ordem_id in enumerate(ordens_ids, start=1)
    ]
    ItemRota.objects.bulk_create(itens)


def _auditar_criacao(rota: Rota, ordens_ids: list[int], autoria: Autoria) -> None:
    novo = {"nome": rota.nome, "equipe_id": rota.equipe_id, "ordens_ids": ordens_ids}
    alteracao = Alteracao("Rota", rota.pk, "criacao", None, novo)
    registrar_auditoria(rota.planejamento.polo_id, alteracao, autoria)
