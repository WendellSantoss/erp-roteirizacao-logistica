from datetime import timedelta
from decimal import Decimal
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone

from almoxarifado.models import ExecucaoKit
from nucleo.models import (
    Equipe,
    EstadoOS,
    OrdemServico,
    Perfil,
    PerfilUsuario,
    Polo,
    RegistroAuditoria,
    Unidade,
)
from nucleo.services_preparacao import Coordenada

AMBIENTE = {"SENHA_USUARIOS_DEMO": "senha-de-teste"}


def popular():
    call_command("popular_dados_demo", stdout=StringIO())


@mock.patch.dict("os.environ", AMBIENTE)
class PopularDadosDemoTest(TestCase):
    def test_popula_todas_as_tabelas_do_mvp(self):
        popular()
        self.assertEqual(Polo.objects.count(), 3)
        self.assertEqual(PerfilUsuario.objects.count(), 7)
        self.assertEqual(OrdemServico.objects.count(), 90)
        self.assertTrue(RegistroAuditoria.objects.exists())

    def test_rodar_duas_vezes_nao_duplica(self):
        popular()
        popular()
        self.assertEqual(OrdemServico.objects.count(), 90)
        self.assertEqual(
            RegistroAuditoria.objects.count(),
            OrdemServico.objects.filter(estado=EstadoOS.DESCONSIDERADA).count(),
        )

    def test_existe_execucao_de_ontem_para_a_trava_d_menos_1(self):
        popular()
        ontem = timezone.localdate() - timedelta(days=1)
        self.assertTrue(ExecucaoKit.objects.filter(data=ontem, polo__codigo="POLO_1").exists())

    def test_usuario_restrito_so_tem_o_proprio_polo(self):
        popular()
        perfil = PerfilUsuario.objects.get(usuario__username="bruno.norte@genios.test")
        codigos = list(perfil.polos_autorizados.values_list("codigo", flat=True))
        self.assertEqual(codigos, ["POLO_2"])

    def test_usuario_consegue_autenticar_com_a_senha_do_ambiente(self):
        popular()
        logou = self.client.login(username="ana.analista@genios.test", password="senha-de-teste")
        self.assertTrue(logou)


class PopularDadosDemoSemSenhaTest(TestCase):
    @mock.patch.dict("os.environ", {}, clear=True)
    def test_sem_senha_no_ambiente_falha_sem_gravar(self):
        with self.assertRaises(CommandError):
            popular()
        self.assertFalse(Polo.objects.exists())


@mock.patch.dict("os.environ", AMBIENTE)
class DadosDoRoteirizadorTest(TestCase):
    def test_unidades_com_coordenada_ficam_na_area_de_operacao(self):
        popular()
        for unidade in Unidade.objects.filter(latitude__isnull=False):
            coordenada = Coordenada(unidade.latitude, unidade.longitude)
            self.assertTrue(coordenada.dentro_da_area, unidade.nome)

    def test_ha_unidade_sem_coordenada_para_a_hu024(self):
        popular()
        self.assertTrue(Unidade.objects.filter(no_escopo=True, latitude__isnull=True).exists())

    def test_coordenada_manual_nao_e_sobrescrita(self):
        popular()
        unidade = Unidade.objects.get(codigo="UN-108")
        unidade.latitude, unidade.longitude = Decimal("-7.1"), Decimal("-34.9")
        unidade.coordenada_manual = True
        unidade.save()
        popular()
        unidade.refresh_from_db()
        self.assertEqual(unidade.latitude, Decimal("-7.1"))

    def test_existe_coordenador_e_equipes_com_capacidade(self):
        popular()
        self.assertTrue(PerfilUsuario.objects.filter(perfil=Perfil.COORDENADOR).exists())
        self.assertFalse(Equipe.objects.filter(placa="").exists())

    def test_toda_os_apta_tem_coordenada(self):
        popular()
        aptas = OrdemServico.objects.filter(estado=EstadoOS.APTA_A_ROTEIRIZAR)
        self.assertTrue(aptas.exists())
        self.assertFalse(aptas.filter(unidade__latitude__isnull=True).exists())
