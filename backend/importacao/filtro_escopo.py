"""Filtro de escopo contratual (HU-003). ``FiltroEscopo`` do C4 nível 4.

RN-03: OS fora de escopo não é gravada, mas entra no resumo e no log de alertas.
"""

from collections import Counter
from dataclasses import dataclass, field

from importacao.leitor_planilha import Alerta, LinhaPlanilha, normalizar
from nucleo import consultas
from nucleo.upsert import DadosGSAN


@dataclass
class ResultadoEscopo:
    no_escopo: list[DadosGSAN] = field(default_factory=list)
    fora_escopo: int = 0
    alertas: list[Alerta] = field(default_factory=list)


def _indice_de_unidades(polo_id: int) -> dict:
    """Unidades do polo por código e por nome normalizados: a planilha pode trazer qualquer um."""
    indice = {}
    for unidade in consultas.unidades_do_polo(polo_id):
        indice[normalizar(unidade.codigo)] = unidade
        indice[normalizar(unidade.nome)] = unidade
    return indice


def _dados_gsan(linha: LinhaPlanilha, unidade_id: int) -> DadosGSAN:
    valores = {campo: valor for campo, valor in linha.valores.items() if campo != "unidade"}
    return DadosGSAN(unidade_id=unidade_id, **valores)


def filtrar_escopo(polo_id: int, linhas: list[LinhaPlanilha]) -> ResultadoEscopo:
    """Separa as OSs do escopo do polo selecionado (RN-L01) e agrupa as descartadas (CA02)."""
    unidades = _indice_de_unidades(polo_id)
    resultado = ResultadoEscopo()
    descartadas: Counter = Counter()
    primeira_linha: dict[tuple[str, bool], int] = {}
    for linha in linhas:
        nome_unidade = linha.valores["unidade"]
        unidade = unidades.get(normalizar(nome_unidade))
        if unidade is not None and unidade.no_escopo:
            resultado.no_escopo.append(_dados_gsan(linha, unidade.pk))
            continue
        chave = (nome_unidade, unidade is not None)
        descartadas[chave] += 1
        primeira_linha.setdefault(chave, linha.linha)
    resultado.fora_escopo = sum(descartadas.values())
    resultado.alertas = [
        _alerta_de_descarte(chave, total, primeira_linha[chave])
        for chave, total in descartadas.items()
    ]
    return resultado


def _alerta_de_descarte(chave: tuple[str, bool], total: int, linha: int) -> Alerta:
    nome_unidade, cadastrada = chave
    situacao = "fora do escopo do polo" if cadastrada else "não cadastrada"
    return Alerta(linha, "unidade", f"Unidade {nome_unidade} {situacao} — {total} OSs ignoradas")
