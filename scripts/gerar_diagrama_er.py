"""Gera docs/banco/diagrama-er.png a partir dos models Django (fonte única: o código).

Uso (na pasta backend, com o venv ativo e DATABASE_URL definido):
    python ../scripts/gerar_diagrama_er.py | dot -Tpng -Gdpi=110 -o ../docs/banco/diagrama-er.png
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.apps import apps  # noqa: E402
from django.db import connection  # noqa: E402

APPS_DO_MVP = ("nucleo", "importacao", "almoxarifado")
CAMPOS_DO_USUARIO = ("id", "username", "email", "first_name", "password", "is_active")


def tabela_html(model) -> str:
    linhas = [f'<tr><td bgcolor="#dbe8f7" colspan="2"><b>{model._meta.db_table}</b></td></tr>']
    for campo in model._meta.concrete_fields:
        if model._meta.app_label == "auth" and campo.name not in CAMPOS_DO_USUARIO:
            continue
        marca = "PK" if campo.primary_key else ("FK" if campo.is_relation else "")
        tipo = f"{campo.db_type(connection) or ''} {marca}"
        linhas.append(
            f'<tr><td align="left">{campo.column}</td>'
            f'<td align="left"><font color="#555555">{tipo}</font></td></tr>'
        )
    return f'<<table border="0" cellborder="1" cellspacing="0">{"".join(linhas)}</table>>'


def main() -> None:
    models = [m for m in apps.get_models() if m._meta.app_label in APPS_DO_MVP]
    models.append(apps.get_model("auth", "User"))
    saida = ["digraph ER {", "rankdir=LR; node [shape=plaintext, fontname=Helvetica, fontsize=10];"]
    for model in models:
        saida.append(f"{model._meta.db_table} [label={tabela_html(model)}];")
    tabelas = {m._meta.db_table for m in models}
    for model in models:
        for campo in model._meta.get_fields():
            if not campo.is_relation or campo.related_model._meta.db_table not in tabelas:
                continue
            if campo.many_to_one and campo.concrete or campo.one_to_one and campo.concrete:
                alvo = campo.related_model._meta.db_table
                rotulo = f'[label="{campo.name}", fontsize=8]'
                saida.append(f"{model._meta.db_table} -> {alvo} {rotulo};")
            elif campo.many_to_many and campo.concrete:
                alvo = campo.related_model._meta.db_table
                saida.append(f"{model._meta.db_table} -> {alvo} [dir=both, style=dashed];")
    saida.append("}")
    sys.stdout.write("\n".join(saida))


if __name__ == "__main__":
    main()
