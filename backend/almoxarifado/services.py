"""Saída de kits com trava de histórico (HU-016, RN-11).

RN-11: a soma das saídas do kit no polo no dia D, contando a que está sendo pedida, não pode
passar do que foi executado em D−1. A trava vale no servidor (RNF-08).
"""

from dataclasses import asdict, dataclass
from datetime import date, timedelta

from django.db import transaction
from django.utils import timezone

from almoxarifado import consultas
from almoxarifado.excecoes import TravaHistoricoExcedida
from almoxarifado.models import SaidaKit
from nucleo import consultas as consultas_nucleo
from nucleo.excecoes import EntradaInvalida, PoloNaoAutorizado, RecursoNaoEncontrado
from nucleo.services import Alteracao, Autoria, registrar_auditoria


@dataclass(frozen=True)
class PedidoSaida:
    polo_id: int
    equipe_id: int
    kit_id: int
    quantidade: int


@dataclass(frozen=True)
class AvaliacaoTrava:
    tipo_kit: str
    quantidade_solicitada: int
    ja_retirado_hoje: int
    limite_executado_ontem: int

    @property
    def solicitado_hoje(self) -> int:
        return self.ja_retirado_hoje + self.quantidade_solicitada

    @property
    def permitida(self) -> bool:
        return self.solicitado_hoje <= self.limite_executado_ontem


def dia_anterior(dia: date) -> date:
    """D−1 é o dia corrido anterior (dúvida aberta na HU-016; o seed cobre todos os dias)."""
    return dia - timedelta(days=1)


def registrar_saida_kit(pedido: PedidoSaida, usuario) -> SaidaKit:
    """Registra a saída ou recusa com 422; a tentativa recusada fica na auditoria (CA08)."""
    hoje = timezone.localdate()
    with transaction.atomic():
        kit = _validar_pedido(pedido)
        avaliacao = _avaliar_trava(pedido, kit, hoje)
        if avaliacao.permitida:
            return SaidaKit.objects.create(
                polo_id=pedido.polo_id,
                equipe_id=pedido.equipe_id,
                tipo_kit=kit,
                quantidade=pedido.quantidade,
                data=hoje,
                registrado_por=usuario,
            )
        mensagem = _mensagem_de_bloqueio(kit.nome, avaliacao)
        _auditar_tentativa(pedido, avaliacao, Autoria(usuario, mensagem))
    # Fora do atomic: a tentativa auditada é gravada e só depois a saída é recusada.
    raise TravaHistoricoExcedida(mensagem, asdict(avaliacao))


def _validar_pedido(pedido: PedidoSaida):
    if pedido.quantidade <= 0:
        raise EntradaInvalida("A quantidade deve ser maior que zero.")
    equipe = consultas_nucleo.equipe_por_id(pedido.equipe_id)
    if equipe is None:
        raise RecursoNaoEncontrado("Equipe não encontrada.")
    if equipe.polo_id != pedido.polo_id:
        raise PoloNaoAutorizado("A equipe pertence a outro polo.")
    if not equipe.ativa:
        raise EntradaInvalida("A equipe está inativa.")
    kit = consultas.tipo_kit_ativo(pedido.kit_id)
    if kit is None:
        raise RecursoNaoEncontrado("Tipo de kit não encontrado.")
    return kit


def _avaliar_trava(pedido: PedidoSaida, kit, hoje: date) -> AvaliacaoTrava:
    # RN-L03: a linha D−1 fica travada até o commit; a segunda saída simultânea espera e soma
    # a primeira. Sem execução em D−1 o limite é 0 (RN-L02) e não há o que travar.
    execucao = consultas.execucao_travada(pedido.polo_id, pedido.kit_id, dia_anterior(hoje))
    return AvaliacaoTrava(
        tipo_kit=kit.codigo,
        quantidade_solicitada=pedido.quantidade,
        ja_retirado_hoje=consultas.total_saidas_do_dia(pedido.polo_id, pedido.kit_id, hoje),
        limite_executado_ontem=execucao.quantidade if execucao else 0,
    )


def _mensagem_de_bloqueio(nome_kit: str, avaliacao: AvaliacaoTrava) -> str:
    # RF-ALM-04 / HU-016 CA02: "Kit Hidrômetro · Solicitado hoje: 11 un. · Executado ontem: 10 un."
    return (
        f"Saída bloqueada: {nome_kit} · Solicitado hoje: {avaliacao.solicitado_hoje} un. · "
        f"Executado ontem: {avaliacao.limite_executado_ontem} un."
    )


def _auditar_tentativa(pedido: PedidoSaida, avaliacao: AvaliacaoTrava, autoria: Autoria) -> None:
    detalhes = {**asdict(avaliacao), "equipe_id": pedido.equipe_id}
    alteracao = Alteracao("SaidaKit", None, "tentativa_bloqueada", None, detalhes)
    registrar_auditoria(pedido.polo_id, alteracao, autoria)


# ── Consultas para a tela ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class LimiteKit:
    kit_id: int
    tipo_kit: str
    nome: str
    executado_dia_anterior: int
    saidas_registradas_hoje: int
    saldo_disponivel_hoje: int


def limites_do_dia(polo_id: int, data: date) -> list[LimiteKit]:
    """Teto de cada kit no dia: executado em D−1 menos o que já saiu no dia."""
    executados = consultas.execucoes_por_kit(polo_id, dia_anterior(data))
    saidas = consultas.saidas_por_kit(polo_id, data)
    limites = []
    for kit in consultas.tipos_kit_ativos():
        executado, retirado = executados.get(kit.pk, 0), saidas.get(kit.pk, 0)
        saldo = max(executado - retirado, 0)
        limites.append(LimiteKit(kit.pk, kit.codigo, kit.nome, executado, retirado, saldo))
    return limites


def listar_saidas(polos_ids: tuple[int, ...], data: date | None) -> list[SaidaKit]:
    """Saídas dos polos selecionados, mais recentes primeiro."""
    return list(consultas.saidas_dos_polos(polos_ids, data))
