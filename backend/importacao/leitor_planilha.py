"""Leitura e validação do layout da planilha GSAN (HU-002). ``LeitorPlanilhaGSAN`` do C4 nível 4.

Coluna obrigatória ausente recusa o arquivo inteiro; linha inválida só vira alerta (RN-L02/L03).
Colunas extras são ignoradas, inclusive as que tragam dado pessoal do cliente (LGPD).
"""

import unicodedata
import zipfile
from dataclasses import dataclass, field
from datetime import date, datetime
from io import BytesIO

from django.utils import timezone
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from importacao.excecoes import CabecalhoInvalido, PlanilhaIlegivel

# HU-008 RN-L02: prazo vazio usa o prazo do contrato. Sem parametrização no MVP (HU-066), 48 h.
PRAZO_PADRAO_HORAS = 48

# campo -> (rótulo do GSAN, apelidos aceitos, tamanho máximo). Comparação sem acento e caixa.
COLUNAS = {
    "numero": ("Ordem de Serviço", ("os", "numero os", "numero da os"), 30),
    "especificacao": ("Especificação", (), 255),
    "tipo": ("Tipo", ("tipo de servico",), 60),
    "numero_imovel": ("Nº do Imóvel", ("numero do imovel", "imovel", "matricula"), 30),
    "unidade": ("Unidade Atual", ("unidade",), 120),
    "cidade": ("Cidade", ("municipio",), 80),
    "setor": ("Setor", (), 10),
    "quadra": ("Quadra", (), 10),
    "prazo_horas": ("Prazo (h)", ("prazo", "prazo horas"), None),
    "abertura": ("Abertura", ("data de abertura",), None),
}
FORMATOS_DE_DATA = ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S")


def normalizar(texto) -> str:
    """'Nº do Imóvel' -> 'no do imovel': sem acento, minúsculo, só letras/números e espaço."""
    sem_acento = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    limpo = "".join(c if c.isalnum() else " " for c in sem_acento.lower())
    return " ".join(limpo.split())


NOMES_ACEITOS = {
    campo: {normalizar(rotulo), *apelidos} for campo, (rotulo, apelidos, _) in COLUNAS.items()
}


class LinhaInvalida(ValueError):
    def __init__(self, campo: str, motivo: str):
        self.campo, self.motivo = campo, motivo
        super().__init__(motivo)


@dataclass(frozen=True)
class Alerta:
    linha: int
    campo: str
    motivo: str


@dataclass(frozen=True)
class LinhaPlanilha:
    linha: int
    valores: dict


@dataclass
class PlanilhaLida:
    linhas: list[LinhaPlanilha] = field(default_factory=list)
    alertas: list[Alerta] = field(default_factory=list)
    total_linhas: int = 0


def _abrir_primeira_aba(conteudo: bytes):
    try:
        livro = load_workbook(BytesIO(conteudo), read_only=True, data_only=True)
    except (InvalidFileException, zipfile.BadZipFile, KeyError, OSError) as erro:
        raise PlanilhaIlegivel() from erro
    return livro.worksheets[0].iter_rows(values_only=True)


def _mapear_cabecalho(cabecalho) -> dict[str, int]:
    """Índice de cada campo obrigatório no cabeçalho; ordem das colunas não importa (RN-L04)."""
    nomes = [normalizar(celula) for celula in cabecalho]
    indices = {}
    for campo, aceitos in NOMES_ACEITOS.items():
        indice = next((i for i, nome in enumerate(nomes) if nome in aceitos), None)
        if indice is not None:
            indices[campo] = indice
    faltantes = [COLUNAS[c][0] for c in COLUNAS if c not in indices]
    if faltantes:
        raise CabecalhoInvalido(
            f"Colunas obrigatórias ausentes: {', '.join(faltantes)}",
            {"colunas_faltantes": faltantes},
        )
    return indices


def _texto(valor) -> str:
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    return "" if valor is None else str(valor).strip()


def _data_hora(valor) -> datetime:
    if isinstance(valor, datetime):
        data_hora = valor
    elif isinstance(valor, date):
        data_hora = datetime(valor.year, valor.month, valor.day)
    else:
        data_hora = _converter_texto_em_data(_texto(valor))
    if timezone.is_naive(data_hora):
        data_hora = timezone.make_aware(data_hora)
    return data_hora


def _converter_texto_em_data(texto: str) -> datetime:
    for formato in FORMATOS_DE_DATA:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            continue
    raise LinhaInvalida("abertura", f"Abertura '{texto}' não é uma data válida.")


def _prazo(valor, alertas: list[str]) -> int:
    texto = _texto(valor).replace(",", ".")
    if not texto:
        alertas.append("Prazo preenchido com valor padrão do contrato.")
        return PRAZO_PADRAO_HORAS
    try:
        prazo = float(texto)
    except ValueError:
        prazo = 0
    if prazo <= 0 or not prazo.is_integer():
        raise LinhaInvalida("prazo_horas", f"Prazo '{texto}' não é um número positivo de horas.")
    return int(prazo)


def _valores_da_linha(celulas, indices: dict[str, int], avisos: list[str]) -> dict:
    valores = {}
    for campo, indice in indices.items():
        bruto = celulas[indice] if indice < len(celulas) else None
        if campo == "abertura":
            valores[campo] = _data_hora(bruto)
        elif campo == "prazo_horas":
            valores[campo] = _prazo(bruto, avisos)
        else:
            valores[campo] = _texto_validado(campo, bruto)
    return valores


def _texto_validado(campo: str, bruto) -> str:
    texto = _texto(bruto)
    tamanho_maximo = COLUNAS[campo][2]
    if campo in {"numero", "unidade"} and not texto:
        raise LinhaInvalida(campo, f"{COLUNAS[campo][0]} vazia.")
    if tamanho_maximo and len(texto) > tamanho_maximo:
        raise LinhaInvalida(campo, f"{COLUNAS[campo][0]} com mais de {tamanho_maximo} caracteres.")
    return texto


def ler_planilha(conteudo: bytes) -> PlanilhaLida:
    """Valida o cabeçalho e converte as linhas. Considera só a primeira aba (dúvida da HU-002)."""
    linhas = _abrir_primeira_aba(conteudo)
    cabecalho = next(linhas, None)
    if cabecalho is None:
        raise CabecalhoInvalido("A planilha está vazia.", {"colunas_faltantes": []})
    indices = _mapear_cabecalho(cabecalho)
    planilha, vistos = PlanilhaLida(), {}
    for numero_linha, celulas in enumerate(linhas, start=2):
        if any(_texto(c) for c in celulas):
            planilha.total_linhas += 1
            _processar_linha(LinhaPlanilha(numero_linha, celulas), indices, planilha, vistos)
    return planilha


def _processar_linha(bruta: LinhaPlanilha, indices, planilha: PlanilhaLida, vistos: dict) -> None:
    avisos: list[str] = []
    try:
        valores = _valores_da_linha(bruta.valores, indices, avisos)
    except LinhaInvalida as erro:
        planilha.alertas.append(Alerta(bruta.linha, erro.campo, erro.motivo))
        return
    numero = valores["numero"]
    if numero in vistos:
        # HU-002 CA04: só a primeira ocorrência da OS no arquivo vale.
        motivo = f"OS {numero} repetida na linha {bruta.linha}"
        planilha.alertas.append(Alerta(bruta.linha, "numero", motivo))
        return
    vistos[numero] = bruta.linha
    planilha.alertas.extend(Alerta(bruta.linha, "prazo_horas", aviso) for aviso in avisos)
    planilha.linhas.append(LinhaPlanilha(bruta.linha, valores))
