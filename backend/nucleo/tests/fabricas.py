"""Criadores mínimos de objetos para os testes de esquema (dados fictícios)."""

from datetime import UTC, datetime

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from nucleo.models import Equipe, OrdemServico, PerfilUsuario, Polo, Unidade

SENHA_TESTE = "senha-de-teste-123"


def criar_polo(codigo: str = "POLO_T") -> Polo:
    return Polo.objects.create(codigo=codigo, nome=f"Polo {codigo}")


def criar_usuario(email: str = "teste@genios.test"):
    return get_user_model().objects.create_user(username=email, email=email, password="x")


def criar_unidade(polo: Polo, codigo: str = "UN-01") -> Unidade:
    return Unidade.objects.create(polo=polo, codigo=codigo, nome="Unidade de teste")


def criar_equipe(polo: Polo, codigo: str = "EQ-01") -> Equipe:
    return Equipe.objects.create(polo=polo, codigo=codigo, nome="Equipe de teste")


def criar_os(unidade: Unidade, numero: str = "100") -> OrdemServico:
    return OrdemServico.objects.create(
        numero=numero,
        polo=unidade.polo,
        unidade=unidade,
        tipo="RELIGACAO_AGUA",
        especificacao="Religação no cavalete",
        abertura=datetime(2026, 11, 15, 10, tzinfo=UTC),
        prazo_horas=24,
    )


def criar_usuario_com_perfil(email: str, perfil: str, polos: list[Polo]):
    """Usuário fictício com perfil e polos autorizados (HU-019/020)."""
    usuario = get_user_model().objects.create_user(
        username=email, email=email, password=SENHA_TESTE, first_name="Usuária", last_name="Teste"
    )
    perfil_usuario = PerfilUsuario.objects.create(usuario=usuario, perfil=perfil)
    perfil_usuario.polos_autorizados.set(polos)
    return usuario


def cliente_autenticado(usuario, polo_id: int | str | None = None):
    """APIClient com ``Authorization: Bearer`` e, se informado, ``X-Polo-Id``."""
    cliente = APIClient()
    token, _ = Token.objects.get_or_create(user=usuario)
    cabecalhos = {"HTTP_AUTHORIZATION": f"Bearer {token.key}"}
    if polo_id is not None:
        cabecalhos["HTTP_X_POLO_ID"] = str(polo_id)
    cliente.credentials(**cabecalhos)
    return cliente
