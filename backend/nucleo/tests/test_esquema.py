from django.db import IntegrityError, ProgrammingError, transaction
from django.test import TestCase

from nucleo.models import EstadoOS, OrdemServico, OrigemAuditoria, RegistroAuditoria
from nucleo.tests.fabricas import criar_os, criar_polo, criar_unidade, criar_usuario


class OrdemServicoEsquemaTest(TestCase):
    def setUp(self):
        self.polo_1 = criar_polo("POLO_1")
        self.unidade = criar_unidade(self.polo_1)

    def test_os_nova_nasce_pendente_e_nao_desconsiderada(self):
        os_ = criar_os(self.unidade)
        self.assertEqual(os_.estado, EstadoOS.PENDENTE)
        self.assertFalse(os_.desconsiderada)

    def test_rn01_numero_repetido_no_mesmo_polo_e_recusado(self):
        criar_os(self.unidade, numero="4471203")
        with self.assertRaises(IntegrityError):
            criar_os(self.unidade, numero="4471203")

    def test_hu004_ca07_mesmo_numero_em_outro_polo_e_outra_os(self):
        unidade_polo_2 = criar_unidade(criar_polo("POLO_2"))
        criar_os(self.unidade, numero="4471203")
        criar_os(unidade_polo_2, numero="4471203")
        self.assertEqual(OrdemServico.objects.filter(numero="4471203").count(), 2)

    def test_estado_fora_da_lista_e_recusado_pelo_banco(self):
        os_ = criar_os(self.unidade)
        with self.assertRaises(IntegrityError):
            OrdemServico.objects.filter(pk=os_.pk).update(estado="CANCELADA")

    def test_prazo_zero_e_recusado(self):
        os_ = criar_os(self.unidade)
        with self.assertRaises(IntegrityError):
            OrdemServico.objects.filter(pk=os_.pk).update(prazo_horas=0)

    def test_campos_gsan_nao_incluem_tratamento_genios(self):
        self.assertTrue({"estado", "prioridade", "equipe"}.isdisjoint(OrdemServico.CAMPOS_GSAN))


class RegistroAuditoriaImutavelTest(TestCase):
    def setUp(self):
        self.registro = RegistroAuditoria.objects.create(
            entidade="OrdemServico",
            entidade_id=1,
            campo="estado",
            valor_anterior="PENDENTE",
            valor_novo="DESCONSIDERADA",
            autor=criar_usuario(),
            origem=OrigemAuditoria.TELA,
        )

    def test_rnf16_update_na_trilha_e_bloqueado(self):
        with self.assertRaises(ProgrammingError), transaction.atomic():
            RegistroAuditoria.objects.filter(pk=self.registro.pk).update(justificativa="x")

    def test_rnf16_delete_na_trilha_e_bloqueado(self):
        with self.assertRaises(ProgrammingError), transaction.atomic():
            RegistroAuditoria.objects.filter(pk=self.registro.pk).delete()

    def test_insert_na_trilha_continua_permitido(self):
        self.assertEqual(RegistroAuditoria.objects.count(), 1)
