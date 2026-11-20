"""Consultas ao banco do núcleo (camada de acesso a dados, AGENTS.md §2)."""

import logging

from django.db import DatabaseError, connection

logger = logging.getLogger(__name__)


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
