"""Operações do contrato citadas na ERS e na HU-011 (catálogo da HU-066 RN-L04).

Não é dado de demonstração: o Roteirizador não funciona sem ao menos uma operação, então o
catálogo nasce com o banco. A manutenção depois é pelo admin até a HU-066 ter tela.
"""

from django.db import migrations

OPERACOES = [("PSS", "PSS"), ("XPT_EXPRESS", "XPT Express"), ("LITORAL", "Litoral")]


def criar_operacoes(apps, schema_editor):
    operacao = apps.get_model("roteirizacao", "Operacao")
    for codigo, nome in OPERACOES:
        operacao.objects.update_or_create(codigo=codigo, defaults={"nome": nome})


class Migration(migrations.Migration):
    dependencies = [("roteirizacao", "0001_initial")]

    operations = [migrations.RunPython(criar_operacoes, migrations.RunPython.noop)]
