"""Consultas ao banco do núcleo (camada de acesso a dados, AGENTS.md §2)."""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import DatabaseError, connection
from django.db.models import Count, DateTimeField, DurationField, ExpressionWrapper, F, Q, Value

from nucleo.models import (
    Equipe,
    EstadoOS,
    OrdemServico,
    PerfilUsuario,
    Polo,
    RegistroAuditoria,
    Unidade,
)

logger = logging.getLogger(__name__)

MAXIMO_REGISTROS_AUDITORIA = 200


def banco_disponivel() -> bool:
    """Executa ``SELECT 1`` e informa se o banco respondeu."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
    except DatabaseError:
        # Detalhe só no log do servidor; nunca devolver str(exc) ao cliente (AGENTS.md §5).
        logger.exception("Health check: banco indisponível")
        return False
    return True


# ── Usuários e polos ──────────────────────────────────────────────────────────


def usuario_por_email(email: str):
    return get_user_model().objects.filter(username__iexact=email).first()


def perfil_de_acesso(usuario) -> PerfilUsuario | None:
    return PerfilUsuario.objects.filter(usuario_id=usuario.pk).first()


def perfil_do_usuario(usuario) -> str | None:
    perfil = perfil_de_acesso(usuario)
    return perfil.perfil if perfil else None


def polos_do_usuario(usuario) -> list[Polo]:
    """Polos autorizados; quem pode visualizar todos recebe todos os polos ativos (HU-020)."""
    perfil = perfil_de_acesso(usuario)
    if perfil is None:
        return []
    if perfil.pode_visualizar_todos:
        return list(Polo.objects.filter(ativo=True))
    return list(perfil.polos_autorizados.filter(ativo=True))


def polos_autorizados_ids(usuario) -> tuple[int, ...]:
    return tuple(polo.pk for polo in polos_do_usuario(usuario))


# ── Ordens de serviço ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class FiltroOrdens:
    polos_ids: tuple[int, ...]
    estado: str
    agora: datetime
    prioridade: bool | None = None
    atrasada: bool | None = None
    busca: str = ""


def _com_vencimento(queryset):
    """Anota ``vencimento = abertura + prazo_horas`` para filtrar e ordenar por atraso no banco."""
    uma_hora = Value(timedelta(hours=1), output_field=DurationField())
    prazo = ExpressionWrapper(F("prazo_horas") * uma_hora, output_field=DurationField())
    return queryset.annotate(
        vencimento=ExpressionWrapper(F("abertura") + prazo, output_field=DateTimeField())
    )


def ordens_filtradas(filtro: FiltroOrdens):
    """OSs do filtro, prioritárias primeiro e depois maior atraso (HU-006 RN-L02)."""
    consulta = _com_vencimento(
        OrdemServico.objects.select_related("polo", "unidade").filter(
            polo_id__in=filtro.polos_ids, estado=filtro.estado
        )
    )
    if filtro.prioridade is not None:
        consulta = consulta.filter(prioridade=filtro.prioridade)
    if filtro.atrasada is not None:
        atrasadas = Q(vencimento__lt=filtro.agora)
        consulta = consulta.filter(atrasadas if filtro.atrasada else ~atrasadas)
    if filtro.busca:
        consulta = consulta.filter(
            Q(numero__icontains=filtro.busca)
            | Q(setor__icontains=filtro.busca)
            | Q(unidade__codigo__icontains=filtro.busca)
            | Q(unidade__nome__icontains=filtro.busca)
        )
    return consulta.order_by("-prioridade", "vencimento", "id")


def contadores_por_estado(polos_ids: tuple[int, ...]) -> dict[str, int]:
    linhas = (
        OrdemServico.objects.filter(polo_id__in=polos_ids)
        .values("estado")
        .annotate(total=Count("id"))
        .order_by("estado")
    )
    return {linha["estado"]: linha["total"] for linha in linhas}


def ordem_para_alterar(ordem_id: int) -> OrdemServico | None:
    """Busca a OS travando a linha até o fim da transação (evita alterações concorrentes)."""
    return OrdemServico.objects.select_for_update().filter(pk=ordem_id).first()


# ── Unidades, equipes e auditoria ─────────────────────────────────────────────


def unidades_do_polo(polo_id: int) -> list[Unidade]:
    return list(Unidade.objects.filter(polo_id=polo_id))


def numeros_existentes(polo_id: int, numeros: list[str]) -> dict[str, OrdemServico]:
    """OSs já gravadas do polo, numa única consulta (risco de desempenho do upsert, CA08)."""
    existentes = OrdemServico.objects.filter(polo_id=polo_id, numero__in=numeros)
    return {ordem.numero: ordem for ordem in existentes}


def equipes_dos_polos(polos_ids: tuple[int, ...], ativa: bool | None):
    consulta = Equipe.objects.filter(polo_id__in=polos_ids)
    if ativa is not None:
        consulta = consulta.filter(ativa=ativa)
    return consulta


def equipe_por_id(equipe_id: int) -> Equipe | None:
    return Equipe.objects.filter(pk=equipe_id).first()


def registros_de_auditoria(polos_ids: tuple[int, ...], entidade: str, entidade_id: int | None):
    consulta = RegistroAuditoria.objects.select_related("autor").filter(polo_id__in=polos_ids)
    if entidade:
        consulta = consulta.filter(entidade=entidade)
    if entidade_id is not None:
        consulta = consulta.filter(entidade_id=entidade_id)
    return consulta.order_by("-registrado_em", "-id")[:MAXIMO_REGISTROS_AUDITORIA]


def unidades_dos_polos(polos_ids: tuple[int, ...], sem_coordenada: bool | None):
    consulta = Unidade.objects.select_related("polo").filter(polo_id__in=polos_ids)
    if sem_coordenada is not None:
        consulta = consulta.filter(latitude__isnull=sem_coordenada)
    return consulta.annotate(total_ordens=Count("ordens_servico")).order_by("polo_id", "codigo")


def unidade_para_alterar(unidade_id: int) -> Unidade | None:
    return Unidade.objects.select_for_update().filter(pk=unidade_id).first()


def ordens_para_alterar(ordens_ids: list[int]) -> list[OrdemServico]:
    """Trava as OSs na ordem do id (evita deadlock entre duas rotas criadas ao mesmo tempo)."""
    consulta = OrdemServico.objects.select_for_update(of=("self",)).select_related("unidade")
    return list(consulta.filter(pk__in=ordens_ids).order_by("id"))


def ordens_aptas_com_coordenada(polo_id: int):
    """RN-04 e RN-08: o mapa só recebe OS apta cuja unidade tem latitude e longitude."""
    return (
        OrdemServico.objects.select_related("unidade")
        .filter(
            polo_id=polo_id,
            estado=EstadoOS.APTA_A_ROTEIRIZAR,
            unidade__latitude__isnull=False,
            unidade__longitude__isnull=False,
        )
        .order_by("-prioridade", "abertura", "id")
    )
