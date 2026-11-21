"""Exception handler único do DRF: todo erro sai no formato do contrato (AGENTS.md §5)."""

from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from nucleo.excecoes import ErroDeNegocio

# Erros do próprio DRF traduzidos para códigos e mensagens do contrato.
CODIGOS_DRF = {
    exceptions.NotAuthenticated: ("NAO_AUTENTICADO", "Faça login para continuar."),
    exceptions.AuthenticationFailed: ("SESSAO_INVALIDA", "Sessão expirada. Entre novamente."),
    exceptions.PermissionDenied: ("ACESSO_NEGADO", "Você não tem acesso a esta área."),
    exceptions.NotFound: ("NAO_ENCONTRADO", "Registro não encontrado."),
    exceptions.MethodNotAllowed: ("METODO_NAO_PERMITIDO", "Operação não permitida."),
    exceptions.ParseError: ("ENTRADA_INVALIDA", "Não foi possível ler os dados enviados."),
    exceptions.UnsupportedMediaType: ("FORMATO_NAO_SUPORTADO", "Formato de envio não suportado."),
}


def corpo_de_erro(codigo: str, mensagem: str, detalhes: dict | None = None) -> dict:
    return {"erro": {"codigo": codigo, "mensagem": mensagem, "detalhes": detalhes or {}}}


def tratar_excecao(exc, context):
    """Converte ``ErroDeNegocio`` e exceções do DRF em ``{"erro": {...}}``."""
    if isinstance(exc, ErroDeNegocio):
        return Response(corpo_de_erro(exc.codigo, exc.mensagem, exc.detalhes), exc.status_http)
    resposta = exception_handler(exc, context)
    if resposta is None:
        return None
    if isinstance(exc, exceptions.ValidationError):
        resposta.data = corpo_de_erro(
            "ENTRADA_INVALIDA", _primeira_mensagem(exc.detail), {"campos": exc.detail}
        )
        resposta.status_code = status.HTTP_400_BAD_REQUEST
        return resposta
    codigo, mensagem = CODIGOS_DRF.get(type(exc), ("ERRO", "Não foi possível concluir a operação."))
    resposta.data = corpo_de_erro(codigo, mensagem)
    return resposta


def _primeira_mensagem(detalhe) -> str:
    """Primeira mensagem legível de um ``ValidationError`` (aninhado em dict/list)."""
    while isinstance(detalhe, dict | list) and detalhe:
        detalhe = next(iter(detalhe.values())) if isinstance(detalhe, dict) else detalhe[0]
    return str(detalhe) if detalhe else "Dados de entrada inválidos."
