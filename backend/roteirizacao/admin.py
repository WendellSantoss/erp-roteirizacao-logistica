from django.contrib import admin

from roteirizacao.models import Operacao


@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    """Catálogo de operações mantido pelo Administrador enquanto a HU-066 não tem tela."""

    list_display = ["codigo", "nome", "ativa"]
