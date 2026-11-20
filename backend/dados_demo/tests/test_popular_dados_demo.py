from datetime import timedelta
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone

from almoxarifado.models import ExecucaoKit
from nucleo.models import EstadoOS, OrdemServico, PerfilUsuario, Polo, RegistroAuditoria

AMBIENTE = {"SENHA_USUARIOS_DEMO": "senha-de-teste"}


def popular():
    call_command("popular_dados_demo", stdout=StringIO())


@mock.patch.dict("os.environ", AMBIENTE)
class PopularDadosDemoTest(TestCase):
    def test_popula_todas_as_tabelas_do_mvp(self):
        popular()
        self.assertEqual(Polo.objects.count(), 3)
        self.assertEqual(PerfilUsuario.objects.count(), 6)
        self.assertEqual(OrdemServico.objects.count(), 48)
        self.assertTrue(RegistroAuditoria.objects.exists())

    def test_rodar_duas_vezes_nao_duplica(self):
        popular()
        popular()
        self.assertEqual(OrdemServico.objects.count(), 48)
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
