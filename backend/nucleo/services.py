"""Regras de negócio do núcleo: ciclo de vida da OS, auditoria e tratamento de pendências.

Nada aqui conhece ``request``/``Response``: as views traduzem HTTP e chamam estas funções.
"""

from dataclasses import dataclass
from datetime import datetime

from django.db import transaction

from nucleo import consultas
from nucleo.excecoes import (
    EntradaInvalida,
    OrdemEmEstadoTerminal,
    PoloNaoAutorizado,
    RecursoNaoEncontrado,
    TransicaoNaoPermitida,
)
from nucleo.models import EstadoOS, OrdemServico, OrigemAuditoria, RegistroAuditoria

ENTIDADE_OS = "OrdemServico"
JUSTIFICATIVA_PADRAO_PRIORIDADE = "Alteração manual de prioridade"
SEGUNDOS_POR_HORA = 3600


@dataclass(frozen=True)
class Autoria:
    """Quem fez a alteração e por quê; vai para a trilha de auditoria."""

    usuario: object
    justificativa: str = ""
    origem: str = OrigemAuditoria.TELA


@dataclass(frozen=True)
class Alteracao:
    entidade: str
    entidade_id: int | None
    campo: str
    valor_anterior: object
    valor_novo: object


def registrar_auditoria(polo_id: int | None, alteracao: Alteracao, autoria: Autoria):
    """Grava um registro na trilha imutável (RNF-16). Chame dentro da transação da alteração."""
    return RegistroAuditoria.objects.create(
        polo_id=polo_id,
        entidade=alteracao.entidade,
        entidade_id=alteracao.entidade_id,
        campo=alteracao.campo,
        valor_anterior=alteracao.valor_anterior,
        valor_novo=alteracao.valor_novo,
        justificativa=autoria.justificativa,
        autor=autoria.usuario,
        origem=autoria.origem,
    )


class CicloDeVidaOS:
    """Único ponto que muda o estado da OS (HU-F11); transição fora da tabela é recusada."""

    TRANSICOES = {
        EstadoOS.PENDENTE: {EstadoOS.APTA_A_ROTEIRIZAR, EstadoOS.DESCONSIDERADA},
        EstadoOS.APTA_A_ROTEIRIZAR: {EstadoOS.ROTEIRIZADA, EstadoOS.DESCONSIDERADA},
        EstadoOS.ROTEIRIZADA: {EstadoOS.APTA_A_ROTEIRIZAR, EstadoOS.DESPACHADA},
        EstadoOS.DESPACHADA: {EstadoOS.EXECUTADA, EstadoOS.INVALIDADA},
        EstadoOS.EXECUTADA: {EstadoOS.VALIDADA, EstadoOS.INVALIDADA},
        EstadoOS.INVALIDADA: {EstadoOS.VALIDADA},
        EstadoOS.VALIDADA: {EstadoOS.FATURADA},
        EstadoOS.FATURADA: {EstadoOS.VALIDADA},
        EstadoOS.DESCONSIDERADA: set(),
    }

    @classmethod
    def permite(cls, origem: str, destino: str) -> bool:
        return destino in cls.TRANSICOES.get(origem, set())

    @classmethod
    def transicionar(cls, ordem: OrdemServico, destino: str, autoria: Autoria) -> OrdemServico:
        """Muda o estado e grava a trilha na mesma transação (regras 4 e 5 do AGENTS.md)."""
        origem = ordem.estado
        if not cls.permite(origem, destino):
            rotulo_origem, rotulo_destino = EstadoOS(origem).label, EstadoOS(destino).label
            raise TransicaoNaoPermitida(
                f"Transição não permitida: {rotulo_origem} → {rotulo_destino}",
                {"estado_atual": origem, "estado_solicitado": destino},
            )
        with transaction.atomic():
            ordem.estado = destino
            ordem.save(update_fields=["estado", "atualizado_em"])
            alteracao = Alteracao(ENTIDADE_OS, ordem.pk, "estado", origem, destino)
            registrar_auditoria(ordem.polo_id, alteracao, autoria)
        return ordem


# ── Prazos e atraso (RN-06) ───────────────────────────────────────────────────


@dataclass(frozen=True)
class Prazos:
    tempo_decorrido_horas: float
    atraso_horas: float
    em_atraso: bool


def calcular_prazos(abertura: datetime, prazo_horas: int, agora: datetime) -> Prazos:
    """RN-06: atraso = (agora − abertura) − prazo. Só é atraso quando passa de zero (HU-008 CA02).

    Valor negativo de ``atraso_horas`` é o tempo que ainda falta para vencer.
    """
    decorrido = (agora - abertura).total_seconds() / SEGUNDOS_POR_HORA
    atraso = decorrido - prazo_horas
    return Prazos(round(decorrido, 2), round(atraso, 2), atraso > 0)


# ── Pendências (HU-006/007/008) ───────────────────────────────────────────────

FiltroOrdens = consultas.FiltroOrdens


@dataclass(frozen=True)
class PaginaOrdens:
    total: int
    contadores_por_status: dict[str, int]
    itens: list[tuple[OrdemServico, Prazos]]


def listar_ordens(filtro: consultas.FiltroOrdens, pagina: int, tamanho: int) -> PaginaOrdens:
    """Lista paginada com decorrido e atraso calculados no servidor (HU-008 RN-L04)."""
    consulta = consultas.ordens_filtradas(filtro)
    inicio = (pagina - 1) * tamanho
    itens = [
        (ordem, calcular_prazos(ordem.abertura, ordem.prazo_horas, filtro.agora))
        for ordem in consulta[inicio : inicio + tamanho]
    ]
    contadores = consultas.contadores_por_estado(filtro.polos_ids)
    return PaginaOrdens(consulta.count(), contadores, itens)


def _ordem_do_polo(ordem_id: int, polo_id: int) -> OrdemServico:
    ordem = consultas.ordem_para_alterar(ordem_id)
    if ordem is None:
        raise RecursoNaoEncontrado("Ordem de serviço não encontrada.")
    if ordem.polo_id != polo_id:
        raise PoloNaoAutorizado("A OS pertence a outro polo.")
    return ordem


ESTADOS_SEM_ALTERACAO = {EstadoOS.DESCONSIDERADA, EstadoOS.FATURADA}


@transaction.atomic
def marcar_prioridade(ordem_id: int, polo_id: int, prioridade: bool, autoria: Autoria):
    """Marca/desmarca prioridade; a reimportação preserva o valor (HU-004 CA02)."""
    ordem = _ordem_do_polo(ordem_id, polo_id)
    if ordem.estado in ESTADOS_SEM_ALTERACAO:
        raise OrdemEmEstadoTerminal(
            f"A OS {ordem.numero} está {EstadoOS(ordem.estado).label.lower()} e não pode mudar."
        )
    if ordem.prioridade == prioridade:
        return ordem
    anterior = ordem.prioridade
    ordem.prioridade = prioridade
    ordem.save(update_fields=["prioridade", "atualizado_em"])
    justificativa = autoria.justificativa.strip() or JUSTIFICATIVA_PADRAO_PRIORIDADE
    autoria = Autoria(autoria.usuario, justificativa, autoria.origem)
    alteracao = Alteracao(ENTIDADE_OS, ordem.pk, "prioridade", anterior, prioridade)
    registrar_auditoria(ordem.polo_id, alteracao, autoria)
    return ordem


@transaction.atomic
def desconsiderar_os(ordem_id: int, polo_id: int, autoria: Autoria) -> OrdemServico:
    """Leva a OS ao estado terminal Desconsiderada (RN-07) com justificativa obrigatória."""
    if not autoria.justificativa.strip():
        raise EntradaInvalida("Informe a justificativa para desconsiderar a OS.")
    ordem = _ordem_do_polo(ordem_id, polo_id)
    return CicloDeVidaOS.transicionar(ordem, EstadoOS.DESCONSIDERADA, autoria)


# ── Consultas de apoio (auditoria e equipes) ──────────────────────────────────


def consultar_auditoria(polos_ids: tuple[int, ...], entidade: str, entidade_id: int | None):
    """Trilha dos polos do usuário, do mais recente para o mais antigo (HU-045)."""
    return list(consultas.registros_de_auditoria(polos_ids, entidade, entidade_id))


def listar_equipes(polos_ids: tuple[int, ...], ativa: bool | None):
    """Equipes dos polos selecionados, para o formulário de saída de kit (contrato §6)."""
    return list(consultas.equipes_dos_polos(polos_ids, ativa))
