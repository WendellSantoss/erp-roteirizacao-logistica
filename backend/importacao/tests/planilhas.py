"""Gera planilhas GSAN fictícias em memória para os testes de importação."""

from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from openpyxl import Workbook

CABECALHO = [
    "Ordem de Serviço",
    "Especificação",
    "Tipo",
    "Nº do Imóvel",
    "Data de Geração",
    "Unidade Atual",
    "Cidade",
    "Setor",
    "Quadra",
    "Prazo (h)",
    "Abertura",
]


def linha_gsan(numero: str, unidade: str = "UN-01", **campos) -> dict:
    """Uma linha válida; ``campos`` sobrescreve qualquer coluna pelo rótulo sem espaço."""
    linha = {
        "Ordem de Serviço": numero,
        "Especificação": "Religação no cavalete",
        "Tipo": "RELIGACAO_AGUA",
        "Nº do Imóvel": "123",
        "Data de Geração": "10/11/2026 08:00",
        "Unidade Atual": unidade,
        "Cidade": "Cidade Demo",
        "Setor": "012",
        "Quadra": "045",
        "Prazo (h)": 24,
        "Abertura": "10/11/2026 08:00",
    }
    linha.update(campos)
    return linha


def planilha_xlsx(linhas: list[dict], cabecalho: list[str] | None = None) -> bytes:
    cabecalho = cabecalho or CABECALHO
    livro = Workbook()
    aba = livro.active
    aba.append(cabecalho)
    for linha in linhas:
        aba.append([linha.get(coluna) for coluna in cabecalho])
    saida = BytesIO()
    livro.save(saida)
    return saida.getvalue()


def arquivo(conteudo: bytes, nome: str = "gsan_os.xlsx") -> SimpleUploadedFile:
    tipo = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return SimpleUploadedFile(nome, conteudo, content_type=tipo)
