"""Consultas do almoxarifado (camada de acesso a dados)."""

from datetime import date

from django.db.models import Sum

from almoxarifado.models import ExecucaoKit, SaidaKit, TipoKit


def tipo_kit_ativo(kit_id: int) -> TipoKit | None:
    return TipoKit.objects.filter(pk=kit_id, ativo=True).first()


def tipos_kit_ativos() -> list[TipoKit]:
    return list(TipoKit.objects.filter(ativo=True))


def execucao_travada(polo_id: int, kit_id: int, data: date) -> ExecucaoKit | None:
    """Trava a linha de execução D-1 até o fim da transação (HU-016 RN-L03, concorrência)."""
    return (
        ExecucaoKit.objects.select_for_update()
        .filter(polo_id=polo_id, tipo_kit_id=kit_id, data=data)
        .first()
    )


def total_saidas_do_dia(polo_id: int, kit_id: int, data: date) -> int:
    soma = SaidaKit.objects.filter(polo_id=polo_id, tipo_kit_id=kit_id, data=data).aggregate(
        total=Sum("quantidade")
    )
    return soma["total"] or 0


def execucoes_por_kit(polo_id: int, data: date) -> dict[int, int]:
    linhas = ExecucaoKit.objects.filter(polo_id=polo_id, data=data)
    return {linha.tipo_kit_id: linha.quantidade for linha in linhas}


def saidas_por_kit(polo_id: int, data: date) -> dict[int, int]:
    linhas = (
        SaidaKit.objects.filter(polo_id=polo_id, data=data)
        .values("tipo_kit_id")
        .annotate(total=Sum("quantidade"))
        .order_by("tipo_kit_id")
    )
    return {linha["tipo_kit_id"]: linha["total"] for linha in linhas}


def saidas_dos_polos(polos_ids: tuple[int, ...], data: date | None):
    consulta = SaidaKit.objects.select_related("polo", "equipe", "tipo_kit", "registrado_por")
    consulta = consulta.filter(polo_id__in=polos_ids)
    if data is not None:
        consulta = consulta.filter(data=data)
    return consulta.order_by("-registrado_em", "-id")
