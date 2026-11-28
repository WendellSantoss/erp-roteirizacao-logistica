"""Erros de negócio do GeniOS (AGENTS.md §5).

Cada exceção carrega o código, a mensagem para o usuário e o status HTTP do contrato. Os services
só levantam estas exceções; quem as converte em resposta é ``nucleo.tratamento_erros``.
"""


class ErroDeNegocio(Exception):
    """Base de todos os erros de negócio, já no formato ``{"erro": {...}}`` do contrato."""

    status_http = 400
    codigo = "ERRO_DE_NEGOCIO"
    mensagem_padrao = "Não foi possível concluir a operação."

    def __init__(self, mensagem: str | None = None, detalhes: dict | None = None):
        self.mensagem = mensagem or self.mensagem_padrao
        self.detalhes = detalhes or {}
        super().__init__(self.mensagem)


class EntradaInvalida(ErroDeNegocio):
    codigo = "ENTRADA_INVALIDA"
    mensagem_padrao = "Dados de entrada inválidos."


class PoloObrigatorio(ErroDeNegocio):
    codigo = "POLO_OBRIGATORIO"
    mensagem_padrao = "Selecione um polo específico para esta operação."


class PoloNaoAutorizado(ErroDeNegocio):
    status_http = 403
    codigo = "POLO_NAO_AUTORIZADO"
    mensagem_padrao = "Você não tem acesso a este polo."


class AcessoNegado(ErroDeNegocio):
    status_http = 403
    codigo = "ACESSO_NEGADO"
    mensagem_padrao = "Você não tem acesso a esta área."


class RecursoNaoEncontrado(ErroDeNegocio):
    status_http = 404
    codigo = "NAO_ENCONTRADO"
    mensagem_padrao = "Registro não encontrado."


class CredenciaisInvalidas(ErroDeNegocio):
    status_http = 401
    codigo = "CREDENCIAIS_INVALIDAS"
    # HU-019 RN-L05: a mensagem não revela se o e-mail existe.
    mensagem_padrao = "E-mail ou senha inválidos"


class LoginBloqueado(ErroDeNegocio):
    status_http = 429
    codigo = "LOGIN_BLOQUEADO"
    mensagem_padrao = "Muitas tentativas. Tente novamente em 15 minutos"


class TransicaoNaoPermitida(ErroDeNegocio):
    status_http = 409
    codigo = "TRANSICAO_NAO_PERMITIDA"


class OrdemEmEstadoTerminal(ErroDeNegocio):
    status_http = 409
    codigo = "OS_EM_ESTADO_TERMINAL"
    mensagem_padrao = "A OS está em um estado que não permite alteração."


class CoordenadaForaDaArea(ErroDeNegocio):
    status_http = 422
    codigo = "COORDENADA_FORA_DA_AREA"
    # HU-024 CA03 / HU-005 RN-L02.
    mensagem_padrao = "Coordenada fora da área de operação (Paraíba)"


class OrdensInaptas(ErroDeNegocio):
    """RN-08: só OS apta, com coordenada e não desconsiderada entra em rota."""

    status_http = 422
    codigo = "OS_INAPTA_PARA_ROTA"
