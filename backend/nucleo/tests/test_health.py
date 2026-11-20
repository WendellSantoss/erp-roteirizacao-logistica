from unittest import mock

from django.db import OperationalError
from django.test import TestCase


class HealthCheckTest(TestCase):
    def test_banco_ok_responde_200(self):
        resposta = self.client.get("/health")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), {"status": "API OK", "database": "Banco OK"})

    def test_banco_fora_responde_503_sem_vazar_detalhe(self):
        with mock.patch("nucleo.consultas.connection.cursor", side_effect=OperationalError("x")):
            resposta = self.client.get("/health")
        self.assertEqual(resposta.status_code, 503)
        self.assertEqual(resposta.json(), {"status": "API OK", "database": "Erro no banco"})
