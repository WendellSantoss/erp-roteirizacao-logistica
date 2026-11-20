"""Criadores mínimos de objetos para os testes de esquema (dados fictícios)."""

from datetime import UTC, datetime

from django.contrib.auth import get_user_model

from nucleo.models import Equipe, OrdemServico, Polo, Unidade


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
