"""Regras da preparação da carteira para o mapa (HU-024, HU-060) e transições em lote da OS.

Fica separado de ``services.py`` para manter cada arquivo abaixo de 300 linhas (AGENTS.md §4).
Os módulos de negócio (ex.: ``roteirizacao``) mudam o estado das OSs só por aqui: o núcleo é o
dono da tabela de OS (regra 3 do AGENTS.md) e toda mudança passa pelo ``CicloDeVidaOS``.
"""

from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from nucleo import consultas
from nucleo.excecoes import (
    CoordenadaForaDaArea,
    OrdensInaptas,
    PoloNaoAutorizado,
    RecursoNaoEncontrado,
)
from nucleo.models import EstadoOS, OrdemServico, Unidade
from nucleo.services import Alteracao, Autoria, CicloDeVidaOS, registrar_auditoria

# HU-005 RN-L02: área de operação (Paraíba). Fora disso a coordenada é rejeitada.
LATITUDE_MINIMA, LATITUDE_MAXIMA = Decimal("-8.5"), Decimal("-6.0")
LONGITUDE_MINIMA, LONGITUDE_MAXIMA = Decimal("-38.8"), Decimal("-34.7")
ENTIDADE_UNIDADE = "Unidade"
MOTIVO_SEM_COORDENADA = "sem coordenada"
MOTIVO_ESTADO = "não está pendente"


# ── Coordenada manual (HU-024) ────────────────────────────────────────────────


@dataclass(frozen=True)
class Coordenada:
    latitude: Decimal
    longitude: Decimal

    @property
    def dentro_da_area(self) -> bool:
        latitude_ok = LATITUDE_MINIMA <= self.latitude <= LATITUDE_MAXIMA
        return latitude_ok and LONGITUDE_MINIMA <= self.longitude <= LONGITUDE_MAXIMA


def listar_unidades(polos_ids: tuple[int, ...], sem_coordenada: bool | None) -> list[Unidade]:
    """Unidades dos polos do usuário; ``sem_coordenada`` mostra só as que faltam resolver."""
    return list(consultas.unidades_dos_polos(polos_ids, sem_coordenada))


@transaction.atomic
def informar_coordenada(unidade_id: int, polo_id: int, coordenada: Coordenada, autoria: Autoria):
    """Grava a coordenada como manual e registra anterior → nova na trilha (HU-024 RN-L03)."""
    if not coordenada.dentro_da_area:
        raise CoordenadaForaDaArea()
    unidade = consultas.unidade_para_alterar(unidade_id)
    if unidade is None:
        raise RecursoNaoEncontrado("Unidade não encontrada.")
    if unidade.polo_id != polo_id:
        raise PoloNaoAutorizado("A unidade pertence a outro polo.")
    anterior = _coordenada_como_texto(unidade.latitude, unidade.longitude)
    unidade.latitude, unidade.longitude = coordenada.latitude, coordenada.longitude
    unidade.coordenada_manual = True
    unidade.save(update_fields=["latitude", "longitude", "coordenada_manual"])
    nova = _coordenada_como_texto(coordenada.latitude, coordenada.longitude)
    alteracao = Alteracao(ENTIDADE_UNIDADE, unidade.pk, "coordenada", anterior, nova)
    registrar_auditoria(polo_id, alteracao, autoria)
    return unidade


def _coordenada_como_texto(latitude, longitude) -> dict | None:
    # JSONField não serializa Decimal; texto preserva as 6 casas sem erro de arredondamento.
    if latitude is None or longitude is None:
        return None
    return {"latitude": str(latitude), "longitude": str(longitude)}


# ── Liberação para roteirização (HU-060) ──────────────────────────────────────


@dataclass(frozen=True)
class OrdemRecusada:
    numero: str
    motivo: str


@dataclass(frozen=True)
class ResultadoLiberacao:
    liberadas: list[str]
    nao_liberadas: list[OrdemRecusada]


@transaction.atomic
def liberar_para_roteirizacao(ordens_ids: list[int], polo_id: int, autoria: Autoria):
    """Leva as pendentes com coordenada a "Apta a roteirizar"; as demais são puladas (RN-L02)."""
    ordens = _ordens_do_polo(ordens_ids, polo_id)
    liberadas, recusadas = [], []
    for ordem in ordens:
        motivo = _motivo_para_nao_liberar(ordem)
        if motivo:
            recusadas.append(OrdemRecusada(ordem.numero, motivo))
            continue
        CicloDeVidaOS.transicionar(ordem, EstadoOS.APTA_A_ROTEIRIZAR, autoria)
        liberadas.append(ordem.numero)
    return ResultadoLiberacao(liberadas, recusadas)


def _motivo_para_nao_liberar(ordem: OrdemServico) -> str:
    if ordem.estado != EstadoOS.PENDENTE:
        return MOTIVO_ESTADO
    if not ordem.unidade.tem_coordenada:
        return MOTIVO_SEM_COORDENADA  # RN-04
    return ""


def _ordens_do_polo(ordens_ids: list[int], polo_id: int) -> list[OrdemServico]:
    """Trava as OSs pedidas; id inexistente dá 404 e OS de outro polo dá 403."""
    ordens = consultas.ordens_para_alterar(ordens_ids)
    if len(ordens) != len(set(ordens_ids)):
        raise RecursoNaoEncontrado("Uma ou mais OSs não foram encontradas.")
    if any(ordem.polo_id != polo_id for ordem in ordens):
        raise PoloNaoAutorizado("Há OS de outro polo na seleção.")
    return ordens


# ── Transições pedidas pelo Roteirizador (HU-056, HU-014) ─────────────────────


def ordens_aptas_no_mapa(polo_id: int) -> list[OrdemServico]:
    """OSs que podem aparecer como pin e ser selecionadas (RN-04, RN-08)."""
    return list(consultas.ordens_aptas_com_coordenada(polo_id))


def roteirizar_ordens(ordens_ids: list[int], polo_id: int, autoria: Autoria):
    """Valida RN-08 em todas e só então leva cada OS a "Roteirizada". Use dentro de transação."""
    ordens = _ordens_do_polo(ordens_ids, polo_id)
    inaptas = [ordem.numero for ordem in ordens if not _apta_para_rota(ordem)]
    if inaptas:
        raise OrdensInaptas(
            f"OSs que não estão aptas a roteirizar: {', '.join(inaptas)}",
            {"ordens": inaptas},
        )
    for ordem in ordens:
        CicloDeVidaOS.transicionar(ordem, EstadoOS.ROTEIRIZADA, autoria)
    return ordens


def _apta_para_rota(ordem: OrdemServico) -> bool:
    return ordem.estado == EstadoOS.APTA_A_ROTEIRIZAR and ordem.unidade.tem_coordenada


def despachar_ordens(ordens_ids: list[int], polo_id: int, autoria: Autoria):
    """RN-10: gerar o RPA leva as OSs a "Despachada". Chame dentro da transação da geração."""
    ordens = _ordens_do_polo(ordens_ids, polo_id)
    for ordem in ordens:
        CicloDeVidaOS.transicionar(ordem, EstadoOS.DESPACHADA, autoria)
    return ordens
