"""HU-F11 — máquina de estados da OS (CicloDeVidaOS)."""

import re
from pathlib import Path

from django.test import TestCase

from nucleo.excecoes import TransicaoNaoPermitida
from nucleo.models import EstadoOS, OrdemServico, RegistroAuditoria
from nucleo.services import Autoria, CicloDeVidaOS
from nucleo.tests.fabricas import criar_os, criar_polo, criar_unidade, criar_usuario

# Tabela da HU-F11 (origem, destino), escrita de novo aqui de propósito: o teste confere o código.
TRANSICOES_DA_HISTORIA = {
    ("PENDENTE", "APTA_A_ROTEIRIZAR"),
    ("PENDENTE", "DESCONSIDERADA"),
    ("APTA_A_ROTEIRIZAR", "DESCONSIDERADA"),
    ("APTA_A_ROTEIRIZAR", "ROTEIRIZADA"),
    ("ROTEIRIZADA", "APTA_A_ROTEIRIZAR"),
    ("ROTEIRIZADA", "DESPACHADA"),
    ("DESPACHADA", "EXECUTADA"),
    ("DESPACHADA", "INVALIDADA"),
    ("EXECUTADA", "INVALIDADA"),
    ("EXECUTADA", "VALIDADA"),
    ("INVALIDADA", "VALIDADA"),
    ("VALIDADA", "FATURADA"),
    ("FATURADA", "VALIDADA"),
}


class CicloDeVidaTest(TestCase):
    def setUp(self):
        self.usuario = criar_usuario()
        self.ordem = criar_os(criar_unidade(criar_polo()))

    def _com_estado(self, estado: str) -> OrdemServico:
        OrdemServico.objects.filter(pk=self.ordem.pk).update(estado=estado)
        return OrdemServico.objects.get(pk=self.ordem.pk)

    def test_ca01_transicao_permitida_muda_estado_e_grava_trilha(self):
        CicloDeVidaOS.transicionar(self.ordem, EstadoOS.APTA_A_ROTEIRIZAR, Autoria(self.usuario))
        self.ordem.refresh_from_db()
        self.assertEqual(self.ordem.estado, EstadoOS.APTA_A_ROTEIRIZAR)
        registro = RegistroAuditoria.objects.get(entidade_id=self.ordem.pk, campo="estado")
        self.assertEqual(registro.valor_anterior, EstadoOS.PENDENTE)
        self.assertEqual(registro.valor_novo, EstadoOS.APTA_A_ROTEIRIZAR)
        self.assertEqual(registro.autor, self.usuario)

    def test_ca02_transicao_proibida_e_recusada_sem_mudar_nada(self):
        ordem = self._com_estado(EstadoOS.DESCONSIDERADA)
        with self.assertRaisesMessage(
            TransicaoNaoPermitida, "Transição não permitida: Desconsiderada → Roteirizada"
        ):
            CicloDeVidaOS.transicionar(ordem, EstadoOS.ROTEIRIZADA, Autoria(self.usuario))
        ordem.refresh_from_db()
        self.assertEqual(ordem.estado, EstadoOS.DESCONSIDERADA)
        self.assertFalse(RegistroAuditoria.objects.exists())

    def test_ca03_cada_transicao_permitida_funciona(self):
        for origem, destino in sorted(TRANSICOES_DA_HISTORIA):
            with self.subTest(origem=origem, destino=destino):
                ordem = self._com_estado(origem)
                CicloDeVidaOS.transicionar(ordem, destino, Autoria(self.usuario))
                ordem.refresh_from_db()
                self.assertEqual(ordem.estado, destino)

    def test_ca03_todas_as_demais_combinacoes_sao_recusadas(self):
        for origem in EstadoOS.values:
            for destino in EstadoOS.values:
                if (origem, destino) in TRANSICOES_DA_HISTORIA:
                    continue
                with self.subTest(origem=origem, destino=destino):
                    self.assertFalse(CicloDeVidaOS.permite(origem, destino))


class EstadoSoMudaPeloServicoTest(TestCase):
    """CA04: nenhuma atribuição direta a ``.estado`` fora do CicloDeVidaOS."""

    PERMITIDOS = {"nucleo/services.py"}
    IGNORADOS = ("tests", "migrations", "dados_demo", ".venv")

    def test_ca04_nao_ha_atribuicao_direta_ao_estado(self):
        raiz = Path(__file__).resolve().parents[2]
        atribuicao = re.compile(r"\.estado\s*=[^=]")
        infratores = []
        for arquivo in raiz.rglob("*.py"):
            relativo = arquivo.relative_to(raiz).as_posix()
            if relativo in self.PERMITIDOS or any(p in relativo for p in self.IGNORADOS):
                continue
            if atribuicao.search(arquivo.read_text(encoding="utf-8")):
                infratores.append(relativo)
        self.assertEqual(infratores, [])
