from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from almoxarifado.models import ExecucaoKit, SaidaKit, TipoKit
from nucleo.tests.fabricas import criar_equipe, criar_polo, criar_usuario


class AlmoxarifadoEsquemaTest(TestCase):
    def setUp(self):
        self.polo = criar_polo()
        self.kit = TipoKit.objects.create(codigo="KIT_HIDROMETRO", nome="Kit Hidrômetro")

    def test_execucao_duplicada_no_mesmo_dia_e_recusada(self):
        ExecucaoKit.objects.create(
            polo=self.polo, tipo_kit=self.kit, data=date.today(), quantidade=10
        )
        with self.assertRaises(IntegrityError):
            ExecucaoKit.objects.create(
                polo=self.polo, tipo_kit=self.kit, data=date.today(), quantidade=5
            )

    def test_saida_com_quantidade_zero_e_recusada(self):
        with self.assertRaises(IntegrityError):
            SaidaKit.objects.create(
                polo=self.polo,
                equipe=criar_equipe(self.polo),
                tipo_kit=self.kit,
                quantidade=0,
                data=date.today(),
                registrado_por=criar_usuario(),
            )
