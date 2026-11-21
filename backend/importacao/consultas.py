"""Consultas às tabelas de importação (camada de acesso a dados)."""

from importacao.models import Importacao


def importacao_por_id(importacao_id: int) -> Importacao | None:
    return (
        Importacao.objects.select_related("polo", "usuario")
        .prefetch_related("alertas")
        .filter(pk=importacao_id)
        .first()
    )


def importacoes_dos_polos(polos_ids: tuple[int, ...], status: str):
    consulta = Importacao.objects.select_related("polo", "usuario").filter(polo_id__in=polos_ids)
    if status:
        consulta = consulta.filter(status=status)
    return consulta.order_by("-iniciada_em", "-id")
