"""Autorização por perfil (HU-020) e por polo (cabeçalho ``X-Polo-Id``, contrato §1).

A regra vale no servidor; esconder o botão na tela é só conveniência (HU-020 RN-L01).
"""

from dataclasses import dataclass

from rest_framework.permissions import SAFE_METHODS, BasePermission

from nucleo import consultas
from nucleo.excecoes import AcessoNegado, EntradaInvalida, PoloNaoAutorizado, PoloObrigatorio
from nucleo.models import Perfil

GERENTE = Perfil.GERENTE_CONTRATO
COORDENADOR = Perfil.COORDENADOR
ANALISTA = Perfil.ANALISTA_OPERACOES
ALMOXARIFE = Perfil.ALMOXARIFE
AUDITOR = Perfil.AUDITOR
ADMIN = Perfil.ADMINISTRADOR

# Matriz de acesso da HU-020 restrita aos módulos do MVP: quem vê (V) e quem edita (E).
MATRIZ_ACESSO = {
    "importacao": {"ver": {GERENTE, COORDENADOR}, "editar": {ANALISTA, ADMIN}},
    "pendencias": {"ver": {COORDENADOR, ADMIN}, "editar": {GERENTE, ANALISTA}},
    # O Almoxarife lê as equipes para preencher a saída de kit (contrato §6).
    "equipes": {"ver": {GERENTE, COORDENADOR, ALMOXARIFE}, "editar": {ADMIN}},
    "almoxarifado": {"ver": {GERENTE, COORDENADOR, ADMIN}, "editar": {ALMOXARIFE}},
    "auditoria": {"ver": {GERENTE, ADMIN}, "editar": {AUDITOR}},
}

POLO_TODOS = "TODOS"


def pode_acessar(perfil: str | None, modulo: str, escrita: bool) -> bool:
    regra = MATRIZ_ACESSO[modulo]
    if escrita:
        return perfil in regra["editar"]
    return perfil in regra["ver"] | regra["editar"]


def modulos_visiveis(perfil: str | None) -> list[str]:
    """Módulos que o perfil pode abrir; o frontend usa para montar o menu (HU-020 CA01)."""
    return [modulo for modulo in MATRIZ_ACESSO if pode_acessar(perfil, modulo, escrita=False)]


def modulos_editaveis(perfil: str | None) -> list[str]:
    """Módulos em que o perfil pode gravar; a tela esconde as ações dos demais."""
    return [modulo for modulo in MATRIZ_ACESSO if pode_acessar(perfil, modulo, escrita=True)]


def exige_acesso(modulo: str) -> type[BasePermission]:
    """Cria a permissão DRF do módulo: GET exige "ver"; os demais métodos exigem "editar"."""

    class PermissaoDoModulo(BasePermission):
        def has_permission(self, request, view):
            escrita = request.method not in SAFE_METHODS
            perfil = consultas.perfil_do_usuario(request.user)
            if not pode_acessar(perfil, modulo, escrita):
                raise AcessoNegado()
            return True

    PermissaoDoModulo.__name__ = f"Acesso_{modulo}"
    return PermissaoDoModulo


@dataclass(frozen=True)
class SelecaoPolo:
    """Polo do cabeçalho. ``polo_id`` é ``None`` quando o usuário escolheu "Todos"."""

    polo_id: int | None
    polos_ids: tuple[int, ...]


def selecao_de_polo(request, escrita: bool = False) -> SelecaoPolo:
    """Lê ``X-Polo-Id``. Escrita exige polo específico (400); polo alheio dá 403."""
    valor = request.headers.get("X-Polo-Id", POLO_TODOS).strip().upper()
    autorizados = consultas.polos_autorizados_ids(request.user)
    if valor == POLO_TODOS:
        if escrita:
            raise PoloObrigatorio()
        return SelecaoPolo(None, autorizados)
    if not valor.isdigit():
        raise EntradaInvalida("Cabeçalho X-Polo-Id inválido: use o id do polo ou TODOS.")
    polo_id = int(valor)
    if polo_id not in autorizados:
        raise PoloNaoAutorizado()
    return SelecaoPolo(polo_id, (polo_id,))
