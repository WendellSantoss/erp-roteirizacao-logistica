"""Cenário fictício comum aos testes do Roteirizador."""

from datetime import timedelta

from django.utils import timezone

from nucleo.models import EstadoOS, Perfil
from nucleo.tests.fabricas import (
    cliente_autenticado,
    criar_equipe,
    criar_os,
    criar_polo,
    criar_unidade,
    criar_usuario_com_perfil,
)
from roteirizacao.models import Operacao

URL_PLANEJAMENTO = "/api/v1/roteirizacao/planejamento/"
URL_ROTAS = "/api/v1/roteirizacao/rotas/"
URL_FINALIZAR = "/api/v1/roteirizacao/planejamento/finalizar/"
URL_RPA = "/api/v1/roteirizacao/planejamento/arquivo-rpa/"


def amanha():
    return timezone.localdate() + timedelta(days=1)


def montar(caso):
    """Polo 1 com Equipe A (capacidade 25) e OSs aptas com coordenada; Polo 2 com uma equipe."""
    caso.polo, caso.polo_2 = criar_polo("POLO_1"), criar_polo("POLO_2")
    caso.pss = Operacao.objects.get(codigo="PSS")
    caso.unidade = criar_unidade(caso.polo, "UN-BESSA", com_coordenada=True)
    caso.unidade_sem_coordenada = criar_unidade(caso.polo, "UN-SEM")
    caso.equipe_a = criar_equipe(caso.polo, "EQ-A", capacidade=25)
    caso.equipe_norte = criar_equipe(caso.polo_2, "EQ-N")
    caso.coordenador = criar_usuario_com_perfil(
        "caio@genios.test", Perfil.COORDENADOR, [caso.polo, caso.polo_2]
    )


def criar_aptas(unidade, quantidade: int, prefixo: str = "9") -> list:
    ordens = []
    for indice in range(quantidade):
        ordem = criar_os(unidade, f"{prefixo}{indice:04d}")
        ordem.estado = EstadoOS.APTA_A_ROTEIRIZAR  # estado inicial do cenário, não uma transição
        ordem.save(update_fields=["estado"])
        ordens.append(ordem)
    return ordens


def pedido_rota(caso, ordens, **campos) -> dict:
    corpo = {
        "operacao_id": caso.pss.pk,
        "data": amanha().isoformat(),
        "nome": "Bessa manhã",
        "equipe_id": caso.equipe_a.pk,
        "previsao_inicio": "07:30",
        "carregamento": "07:00",
        "ordens_ids": [ordem.pk for ordem in ordens],
    }
    return {**corpo, **campos}


def cliente(caso, polo=None):
    return cliente_autenticado(caso.coordenador, (polo or caso.polo).pk)


def chave(caso, data=None) -> dict:
    return {"operacao_id": caso.pss.pk, "data": (data or amanha()).isoformat()}


def cliente_autenticado_todos(caso):
    return cliente_autenticado(caso.coordenador, "TODOS")
