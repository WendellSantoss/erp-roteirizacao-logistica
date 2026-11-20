"""Popula o banco com dados fictícios para demonstração e testes manuais (Etapa 4).

Idempotente: pode ser executado várias vezes; usa as chaves naturais para atualizar em vez de
duplicar. Uso: ``SENHA_USUARIOS_DEMO=... python manage.py popular_dados_demo``.
"""

import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from dados_demo import semeadores


class Command(BaseCommand):
    help = "Cria polos, usuários, unidades, equipes, OSs e kits fictícios (idempotente)."

    def handle(self, *args, **options):
        senha = os.getenv("SENHA_USUARIOS_DEMO")
        if not senha:
            raise CommandError("Defina SENHA_USUARIOS_DEMO no ambiente antes de rodar o seed.")
        with transaction.atomic():
            resumo = semeadores.semear_tudo(senha)
        for nome, total in resumo.items():
            self.stdout.write(f"{nome}: {total}")
        self.stdout.write(self.style.SUCCESS("Dados de demonstração prontos."))
