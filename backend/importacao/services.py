"""Importação transacional da planilha GSAN (HU-001 a HU-004). ``ServicoImportacao`` do C4.

Fluxo síncrono no MVP (o Render gratuito não tem worker): recebe → valida layout → filtra escopo →
upsert tudo-ou-nada. O arquivo não é guardado; ficam o nome e o hash SHA-256 (decisão D8).
"""

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.db import DatabaseError, IntegrityError, transaction
from django.utils import timezone

from importacao import consultas
from importacao.excecoes import (
    ArquivoGrandeDemais,
    ArquivoNaoEnviado,
    CabecalhoInvalido,
    FormatoNaoAceito,
    ImportacaoEmAndamento,
    ImportacaoFalhou,
    MaisDeUmArquivo,
    PlanilhaIlegivel,
)
from importacao.filtro_escopo import ResultadoEscopo, filtrar_escopo
from importacao.leitor_planilha import Alerta, ler_planilha
from importacao.models import (
    STATUS_EM_ANDAMENTO,
    AlertaImportacao,
    Importacao,
    StatusImportacao,
)
from nucleo.excecoes import PoloNaoAutorizado, RecursoNaoEncontrado
from nucleo.upsert import upsert_ordens_servico

logger = logging.getLogger(__name__)

EXTENSAO_ACEITA = ".xlsx"
BYTES_POR_MB = 1024 * 1024


@dataclass(frozen=True)
class ArquivoEnviado:
    nome: str
    conteudo: bytes


@dataclass(frozen=True)
class PedidoImportacao:
    arquivo: ArquivoEnviado
    polo_id: int
    usuario: object


def preparar_arquivo(arquivos: list) -> ArquivoEnviado:
    """Confere quantidade, extensão e tamanho antes de registrar a importação (HU-001 CA03-CA08)."""
    if not arquivos:
        raise ArquivoNaoEnviado()
    if len(arquivos) > 1:
        raise MaisDeUmArquivo()
    arquivo = arquivos[0]
    if Path(arquivo.name).suffix.lower() != EXTENSAO_ACEITA:
        raise FormatoNaoAceito()
    limite = settings.LIMITE_PLANILHA_BYTES
    if arquivo.size > limite:
        tamanho_mb, limite_mb = round(arquivo.size / BYTES_POR_MB), limite // BYTES_POR_MB
        mensagem = f"Arquivo com {tamanho_mb} MB excede o limite de {limite_mb} MB"
        raise ArquivoGrandeDemais(mensagem, {"tamanho_bytes": arquivo.size})
    return ArquivoEnviado(arquivo.name, arquivo.read())


def importar_planilha(pedido: PedidoImportacao) -> Importacao:
    """Executa a importação inteira e devolve o registro com o resumo (contrato §4)."""
    importacao = _registrar_inicio(pedido)
    try:
        _processar(importacao, pedido.arquivo)
    finally:
        if importacao.status in STATUS_EM_ANDAMENTO:
            # Erro inesperado: libera o polo para novo envio em vez de travá-lo "em andamento".
            mensagem = ImportacaoFalhou.mensagem_padrao
            _encerrar_sem_gravar(importacao, StatusImportacao.FALHOU, mensagem)
    return importacao


def _processar(importacao: Importacao, arquivo: ArquivoEnviado) -> None:
    try:
        planilha = ler_planilha(arquivo.conteudo)
    except (CabecalhoInvalido, PlanilhaIlegivel) as erro:
        _encerrar_sem_gravar(importacao, StatusImportacao.RECUSADA, erro.mensagem)
        raise
    importacao.total_linhas = planilha.total_linhas
    escopo = filtrar_escopo(importacao.polo_id, planilha.linhas)
    try:
        _gravar(importacao, escopo, [*planilha.alertas, *escopo.alertas])
    except DatabaseError as erro:
        # RNF-07: o atomic desfez tudo; o detalhe vai para o log, não para o usuário.
        logger.exception("Importação %s falhou ao gravar", importacao.pk)
        _encerrar_sem_gravar(importacao, StatusImportacao.FALHOU, ImportacaoFalhou.mensagem_padrao)
        raise ImportacaoFalhou() from erro


def _registrar_inicio(pedido: PedidoImportacao) -> Importacao:
    """Cria o registro em andamento; o índice único parcial garante uma por polo (409)."""
    try:
        with transaction.atomic():
            return Importacao.objects.create(
                polo_id=pedido.polo_id,
                usuario=pedido.usuario,
                nome_arquivo=pedido.arquivo.nome[:255],
                hash_sha256=hashlib.sha256(pedido.arquivo.conteudo).hexdigest(),
                status=StatusImportacao.VALIDANDO,
                etapa="VALIDANDO",
            )
    except IntegrityError as erro:
        raise ImportacaoEmAndamento() from erro


def _gravar(importacao: Importacao, escopo: ResultadoEscopo, alertas: list[Alerta]) -> None:
    with transaction.atomic():
        resultado = upsert_ordens_servico(importacao.polo_id, escopo.no_escopo, importacao.pk)
        AlertaImportacao.objects.bulk_create(
            AlertaImportacao(importacao=importacao, **vars(alerta)) for alerta in alertas
        )
        importacao.novas, importacao.atualizadas = resultado.novas, resultado.atualizadas
        importacao.fora_escopo = escopo.fora_escopo
        _concluir(importacao, StatusImportacao.CONCLUIDA, "")


def _encerrar_sem_gravar(importacao: Importacao, status: str, motivo: str) -> None:
    importacao.novas = importacao.atualizadas = importacao.fora_escopo = 0
    _concluir(importacao, status, motivo)


def _concluir(importacao: Importacao, status: str, motivo: str) -> None:
    importacao.status = status
    importacao.etapa = "FINALIZADA"
    importacao.percentual = 100
    importacao.motivo_falha = motivo
    importacao.concluida_em = timezone.now()
    importacao.save()


def obter_importacao(importacao_id: int, polos_ids: tuple[int, ...]) -> Importacao:
    """Importação de um polo autorizado ao usuário; de outro polo dá 403 (contrato §4)."""
    importacao = consultas.importacao_por_id(importacao_id)
    if importacao is None:
        raise RecursoNaoEncontrado("Importação não encontrada.")
    if importacao.polo_id not in polos_ids:
        raise PoloNaoAutorizado("A importação pertence a um polo não autorizado.")
    return importacao


def listar_importacoes(polos_ids: tuple[int, ...], status: str, pagina: int, tamanho: int):
    """Histórico paginado das importações dos polos selecionados."""
    consulta = consultas.importacoes_dos_polos(polos_ids, status)
    inicio = (pagina - 1) * tamanho
    return consulta.count(), list(consulta[inicio : inicio + tamanho])
