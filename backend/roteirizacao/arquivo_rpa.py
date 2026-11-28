"""Layout do arquivo de despacho para o RPA (HU-014).

A dúvida bloqueante da HU-014 (layout oficial da automação) segue aberta. Este layout é a proposta
do grupo, isolada neste arquivo para que a troca pelo layout real não mexa nas regras:
CSV, separador ``;``, UTF-8, fim de linha CRLF, uma linha por OS, na ordem da rota.
"""

import csv
import hashlib
import io

COLUNAS = [
    "NUMERO_OS",
    "POLO",
    "OPERACAO",
    "DATA_ROTA",
    "ROTA",
    "SEQUENCIA",
    "EQUIPE",
    "PLACA",
    "PREVISAO_INICIO",
    "CARREGAMENTO",
    "TIPO_SERVICO",
    "UNIDADE",
    "LATITUDE",
    "LONGITUDE",
]


def nome_do_arquivo(planejamento) -> str:
    data = planejamento.data.strftime("%Y%m%d")
    return f"rpa_{planejamento.polo.codigo}_{planejamento.operacao.codigo}_{data}.csv"


def montar_conteudo(planejamento, rotas) -> str:
    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=";", lineterminator="\r\n")
    escritor.writerow(COLUNAS)
    for rota in rotas:
        for item in rota.itens.all():
            escritor.writerow(_linha(planejamento, rota, item))
    return saida.getvalue()


def _linha(planejamento, rota, item) -> list:
    ordem = item.ordem_servico
    return [
        ordem.numero,
        planejamento.polo.codigo,
        planejamento.operacao.codigo,
        planejamento.data.isoformat(),
        rota.nome,
        item.sequencia,
        rota.equipe.codigo,
        rota.equipe.placa,
        rota.previsao_inicio.strftime("%H:%M"),
        rota.carregamento.strftime("%H:%M"),
        ordem.tipo,
        ordem.unidade.codigo,
        ordem.unidade.latitude,
        ordem.unidade.longitude,
    ]


def calcular_hash(conteudo: str) -> str:
    """Código de verificação do conteúdo exato do arquivo (HU-014 CA03, RNF-17)."""
    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
