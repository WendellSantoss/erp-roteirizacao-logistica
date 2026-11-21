"""Erros de negócio da importação, com os status HTTP do contrato (§4)."""

from nucleo.excecoes import ErroDeNegocio


class ArquivoNaoEnviado(ErroDeNegocio):
    codigo = "ARQUIVO_NAO_ENVIADO"
    mensagem_padrao = "Envie a planilha do GSAN no campo 'arquivo'."


class MaisDeUmArquivo(ErroDeNegocio):
    codigo = "MAIS_DE_UM_ARQUIVO"
    mensagem_padrao = "Envie um arquivo por vez"


class FormatoNaoAceito(ErroDeNegocio):
    status_http = 422
    codigo = "FORMATO_NAO_ACEITO"
    mensagem_padrao = "Formato não aceito: envie a planilha do GSAN em .xlsx"


class ArquivoGrandeDemais(ErroDeNegocio):
    status_http = 413
    codigo = "ARQUIVO_MUITO_GRANDE"


class CabecalhoInvalido(ErroDeNegocio):
    status_http = 422
    codigo = "CABECALHO_PLANILHA_INVALIDO"


class PlanilhaIlegivel(ErroDeNegocio):
    status_http = 422
    codigo = "PLANILHA_ILEGIVEL"
    mensagem_padrao = "Não foi possível ler a planilha. Gere o arquivo novamente no GSAN"


class ImportacaoEmAndamento(ErroDeNegocio):
    status_http = 409
    codigo = "IMPORTACAO_EM_ANDAMENTO"
    mensagem_padrao = "Já existe uma importação em andamento para este polo."


class ImportacaoFalhou(ErroDeNegocio):
    status_http = 500
    codigo = "IMPORTACAO_FALHOU"
    mensagem_padrao = (
        "A importação falhou e nenhuma OS foi gravada. Tente enviar o arquivo novamente."
    )
