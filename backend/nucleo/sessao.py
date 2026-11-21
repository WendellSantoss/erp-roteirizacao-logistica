"""Regras de login e logout (HU-019). Camada de serviço: não conhece request nem Response."""

from dataclasses import dataclass

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.authtoken.models import Token

from nucleo import consultas
from nucleo.autenticacao import token_expirado
from nucleo.excecoes import CredenciaisInvalidas, LoginBloqueado
from nucleo.permissoes import modulos_editaveis, modulos_visiveis

# HU-019 RN-L02: 5 tentativas erradas seguidas bloqueiam o usuário por 15 minutos.
MAXIMO_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 15 * 60


def _chave_tentativas(email: str) -> str:
    return f"login-falhas:{email.strip().lower()}"


def _registrar_falha(email: str) -> None:
    chave = _chave_tentativas(email)
    cache.set(chave, cache.get(chave, 0) + 1, BLOQUEIO_SEGUNDOS)


def _esta_bloqueado(email: str) -> bool:
    return cache.get(_chave_tentativas(email), 0) >= MAXIMO_TENTATIVAS


@dataclass(frozen=True)
class SessaoAberta:
    token: str
    usuario: object


def entrar(email: str, senha: str) -> SessaoAberta:
    """Autentica por e-mail e senha e devolve o token do turno.

    A mensagem de erro é a mesma para e-mail inexistente e senha errada (RN-L05); usuário
    inativo também não entra (RN-L04, o ``authenticate`` do Django já recusa).
    """
    if _esta_bloqueado(email):
        raise LoginBloqueado()
    usuario = consultas.usuario_por_email(email)
    autenticado = usuario and authenticate(username=usuario.username, password=senha)
    if not autenticado or consultas.perfil_de_acesso(autenticado) is None:
        _registrar_falha(email)
        raise CredenciaisInvalidas()
    cache.delete(_chave_tentativas(email))
    return SessaoAberta(_token_valido(autenticado).key, autenticado)


def _token_valido(usuario) -> Token:
    token, criado = Token.objects.get_or_create(user=usuario)
    if not criado and token_expirado(token.created):
        token.delete()
        token = Token.objects.create(user=usuario)
    return token


def sair(usuario) -> None:
    """Apaga o token: a sessão acaba no servidor, não só no navegador (HU-019 CA05)."""
    Token.objects.filter(user=usuario).delete()


def dados_do_usuario(usuario) -> dict:
    """Dados do cabeçalho: nome, perfil, polos autorizados e módulos do menu (HU-020 CA01)."""
    perfil = consultas.perfil_de_acesso(usuario)
    return {
        "id": usuario.pk,
        "nome": usuario.get_full_name() or usuario.email,
        "email": usuario.email,
        "perfil": perfil.perfil,
        "pode_visualizar_todos": perfil.pode_visualizar_todos,
        "polos_autorizados": consultas.polos_do_usuario(usuario),
        "modulos": modulos_visiveis(perfil.perfil),
        "modulos_editaveis": modulos_editaveis(perfil.perfil),
    }
