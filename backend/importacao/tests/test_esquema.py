from django.db import IntegrityError
from django.test import TestCase

from importacao.models import Importacao, StatusImportacao
from nucleo.tests.fabricas import criar_polo, criar_usuario


class ImportacaoEsquemaTest(TestCase):
    def setUp(self):
        self.polo = criar_polo()
        self.usuario = criar_usuario()

    def _importar(self, status=StatusImportacao.RECEBIDA, polo=None):
        return Importacao.objects.create(
            polo=polo or self.polo,
            usuario=self.usuario,
            nome_arquivo="gsan.xlsx",
            hash_sha256="0" * 64,
            status=status,
        )

    def test_segunda_importacao_em_andamento_no_mesmo_polo_e_recusada(self):
        self._importar(StatusImportacao.GRAVANDO)
        with self.assertRaises(IntegrityError):
            self._importar(StatusImportacao.RECEBIDA)

    def test_importacoes_concluidas_nao_bloqueiam_nova(self):
        self._importar(StatusImportacao.CONCLUIDA)
        self._importar(StatusImportacao.FALHOU)
        self._importar(StatusImportacao.RECEBIDA)
        self.assertEqual(Importacao.objects.count(), 3)

    def test_polos_diferentes_podem_importar_ao_mesmo_tempo(self):
        self._importar(StatusImportacao.GRAVANDO)
        self._importar(StatusImportacao.GRAVANDO, polo=criar_polo("POLO_2"))
        self.assertEqual(Importacao.objects.count(), 2)

    def test_percentual_acima_de_100_e_recusado(self):
        importacao = self._importar()
        with self.assertRaises(IntegrityError):
            Importacao.objects.filter(pk=importacao.pk).update(percentual=101)
