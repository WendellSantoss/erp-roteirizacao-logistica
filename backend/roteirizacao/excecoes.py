"""Erros de negócio do Roteirizador (contrato §7)."""

from nucleo.excecoes import ErroDeNegocio


class RegraDeRotaViolada(ErroDeNegocio):
    """Equipe de outro polo ou inativa (RN-09), capacidade (RN-L03) ou data passada (RN-L04)."""

    status_http = 422
    codigo = "ROTA_INVALIDA"


class OrdemJaEmRota(ErroDeNegocio):
    status_http = 422
    codigo = "OS_JA_EM_ROTA"


class PlanejamentoFinalizado(ErroDeNegocio):
    status_http = 409
    codigo = "PLANEJAMENTO_FINALIZADO"
    mensagem_padrao = "Planejamento finalizado"


class PlanejamentoInconsistente(ErroDeNegocio):
    status_http = 422
    codigo = "PLANEJAMENTO_INCONSISTENTE"
    mensagem_padrao = "O planejamento tem inconsistências; corrija-as antes de finalizar."


class PlanejamentoNaoFinalizado(ErroDeNegocio):
    status_http = 422
    codigo = "PLANEJAMENTO_NAO_FINALIZADO"
    mensagem_padrao = "Finalize o planejamento antes de gerar o RPA"
