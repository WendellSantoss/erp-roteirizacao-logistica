"""Erros de negócio do almoxarifado (contrato §6)."""

from nucleo.excecoes import ErroDeNegocio


class TravaHistoricoExcedida(ErroDeNegocio):
    status_http = 422
    codigo = "TRAVA_HISTORICO_KIT_EXCEDIDA"
