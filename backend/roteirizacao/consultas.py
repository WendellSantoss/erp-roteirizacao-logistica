"""Consultas do Roteirizador (camada de acesso a dados)."""

from datetime import date

from django.db.models import Count, Prefetch

from roteirizacao.models import ArquivoDespacho, ItemRota, Operacao, Planejamento, Rota


def operacoes_ativas() -> list[Operacao]:
    return list(Operacao.objects.filter(ativa=True))


def operacao_ativa(operacao_id: int) -> Operacao | None:
    return Operacao.objects.filter(pk=operacao_id, ativa=True).first()


def planejamento_do_dia(polo_id: int, operacao_id: int, data: date) -> Planejamento | None:
    return (
        Planejamento.objects.select_related("operacao", "finalizado_por")
        .filter(polo_id=polo_id, operacao_id=operacao_id, data=data)
        .first()
    )


def planejamento_para_alterar(polo_id: int, operacao_id: int, data: date) -> Planejamento:
    """Cria o planejamento na primeira rota e trava a linha até o fim da transação.

    A trava serializa criação de rota, finalização e geração do RPA do mesmo planejamento.
    """
    Planejamento.objects.get_or_create(polo_id=polo_id, operacao_id=operacao_id, data=data)
    return (
        Planejamento.objects.select_for_update()
        .select_related("operacao")
        .get(polo_id=polo_id, operacao_id=operacao_id, data=data)
    )


def planejamento_existente_para_alterar(
    polo_id: int, operacao_id: int, data: date
) -> Planejamento | None:
    return (
        Planejamento.objects.select_for_update()
        .select_related("operacao")
        .filter(polo_id=polo_id, operacao_id=operacao_id, data=data)
        .first()
    )


def rotas_do_planejamento(planejamento_id: int) -> list[Rota]:
    itens = ItemRota.objects.select_related("ordem_servico__unidade").order_by("sequencia")
    return list(
        Rota.objects.select_related("equipe")
        .prefetch_related(Prefetch("itens", queryset=itens))
        .filter(planejamento_id=planejamento_id)
        .order_by("previsao_inicio", "id")
    )


def rotas_das_ordens(ordens_ids: list[int]) -> list[tuple[str, str]]:
    """(número da OS, nome da rota) das OSs que já estão em alguma rota (HU-056 CA05)."""
    itens = ItemRota.objects.select_related("rota", "ordem_servico").filter(
        ordem_servico_id__in=ordens_ids
    )
    return [(item.ordem_servico.numero, item.rota.nome) for item in itens.order_by("id")]


def ordens_da_equipe_no_dia(equipe_id: int, data: date) -> int:
    """Total de OSs da equipe no dia em todas as rotas e operações (HU-056 RN-L03)."""
    return ItemRota.objects.filter(rota__equipe_id=equipe_id, rota__planejamento__data=data).count()


def ordens_por_equipe_no_dia(polo_id: int, data: date) -> dict[int, int]:
    linhas = (
        ItemRota.objects.filter(rota__planejamento__polo_id=polo_id, rota__planejamento__data=data)
        .values("rota__equipe_id")
        .annotate(total=Count("id"))
        .order_by("rota__equipe_id")
    )
    return {linha["rota__equipe_id"]: linha["total"] for linha in linhas}


def arquivo_do_planejamento(planejamento_id: int) -> ArquivoDespacho | None:
    return (
        ArquivoDespacho.objects.select_related("gerado_por")
        .filter(planejamento_id=planejamento_id)
        .first()
    )
