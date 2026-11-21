"""Autenticação por token Bearer com validade de um turno (contrato §1, HU-019)."""

from datetime import timedelta

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Contrato §1: o token vale 8 horas (um turno operacional).
VALIDADE_TOKEN = timedelta(hours=8)


def token_expirado(criado_em) -> bool:
    return timezone.now() - criado_em > VALIDADE_TOKEN


class TokenBearerComValidade(TokenAuthentication):
    """Lê ``Authorization: Bearer <token>`` e recusa tokens com mais de 8 horas."""

    keyword = "Bearer"

    def authenticate_credentials(self, key):
        usuario, token = super().authenticate_credentials(key)
        if token_expirado(token.created):
            raise AuthenticationFailed("Sessão expirada.")
        return usuario, token
