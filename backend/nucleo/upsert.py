"""Upsert das OSs vindas do GSAN (HU-004). Serviço público do núcleo, dono da tabela de OS.

O módulo de importação lê e filtra a planilha e chama este serviço; ele não grava a tabela de OS
diretamente (regra 3 do AGENTS.md).
"""

from dataclasses import dataclass
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from nucleo import consultas
from nucleo.models import OrdemServico

TAMANHO_DO_LOTE = 500


@dataclass(frozen=True)
class DadosGSAN:
    """Campos de uma OS que vêm da planilha (``OrdemServico.CAMPOS_GSAN``)."""

    numero: str
    unidade_id: int
    tipo: str
    especificacao: str
    numero_imovel: str
    cidade: str
    setor: str
    quadra: str
    abertura: datetime
    prazo_horas: int


@dataclass(frozen=True)
class ResultadoUpsert:
    novas: int
    atualizadas: int


def _campos_gsan(dados: DadosGSAN) -> dict:
    campos = {
        campo: getattr(dados, campo) for campo in OrdemServico.CAMPOS_GSAN if campo != "unidade"
    }
    campos["unidade_id"] = dados.unidade_id
    return campos


def _nova_ordem(polo_id: int, dados: DadosGSAN, importacao_id: int) -> OrdemServico:
    # RN-L01: OS nova nasce em "Pendente" (default do model; transição "— → Pendente" da HU-F11).
    return OrdemServico(
        numero=dados.numero,
        polo_id=polo_id,
        importacao_origem_id=importacao_id,
        importacao_ultima_id=importacao_id,
        **_campos_gsan(dados),
    )


def _atualizar_campos_gsan(ordem: OrdemServico, dados: DadosGSAN, importacao_id: int) -> None:
    # RN-02: só os campos do GSAN mudam; estado, prioridade e equipe ficam como estão.
    for campo, valor in _campos_gsan(dados).items():
        setattr(ordem, campo, valor)
    ordem.importacao_ultima_id = importacao_id
    ordem.atualizado_em = timezone.now()


CAMPOS_ATUALIZADOS = [
    *OrdemServico.CAMPOS_GSAN,
    "importacao_ultima",
    "atualizado_em",
]


@transaction.atomic
def upsert_ordens_servico(polo_id: int, linhas: list[DadosGSAN], importacao_id: int):
    """Insere as OSs novas e atualiza as existentes do polo, tudo ou nada (RNF-07).

    OSs do polo que não vieram na planilha não são tocadas (RN-L03, "sem amnésia").
    """
    existentes = consultas.numeros_existentes(polo_id, [linha.numero for linha in linhas])
    novas, atualizadas = [], []
    for dados in linhas:
        ordem = existentes.get(dados.numero)
        if ordem is None:
            novas.append(_nova_ordem(polo_id, dados, importacao_id))
        else:
            _atualizar_campos_gsan(ordem, dados, importacao_id)
            atualizadas.append(ordem)
    OrdemServico.objects.bulk_create(novas, batch_size=TAMANHO_DO_LOTE)
    OrdemServico.objects.bulk_update(atualizadas, CAMPOS_ATUALIZADOS, batch_size=TAMANHO_DO_LOTE)
    return ResultadoUpsert(len(novas), len(atualizadas))
