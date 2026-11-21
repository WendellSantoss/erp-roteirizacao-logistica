"""HU-019 — login individual, sessão de 8 h e logout (contrato §3)."""

from datetime import timedelta
from unittest import mock

from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from nucleo.models import Perfil
from nucleo.tests.fabricas import (
    SENHA_TESTE,
    cliente_autenticado,
    criar_polo,
    criar_usuario_com_perfil,
)

URL_LOGIN = "/api/v1/auth/login/"
URL_ME = "/api/v1/auth/me/"
URL_LOGOUT = "/api/v1/auth/logout/"
EMAIL = "ana.teste@genios.test"


class LoginTest(TestCase):
    def setUp(self):
        cache.clear()
        self.polo = criar_polo("POLO_1")
        self.usuario = criar_usuario_com_perfil(EMAIL, Perfil.ANALISTA_OPERACOES, [self.polo])
        self.cliente = APIClient()

    def entrar(self, email=EMAIL, senha=SENHA_TESTE):
        return self.cliente.post(URL_LOGIN, {"email": email, "senha": senha}, format="json")

    def test_ca01_login_devolve_token_nome_perfil_e_polos(self):
        resposta = self.entrar()
        self.assertEqual(resposta.status_code, 200)
        corpo = resposta.json()
        self.assertTrue(corpo["access_token"])
        self.assertEqual(corpo["usuario"]["nome"], "Usuária Teste")
        self.assertEqual(corpo["usuario"]["perfil"], Perfil.ANALISTA_OPERACOES)
        self.assertEqual(corpo["usuario"]["polos_autorizados"][0]["codigo"], "POLO_1")
        self.assertIn("pendencias", corpo["usuario"]["modulos"])
        self.assertCountEqual(corpo["usuario"]["modulos_editaveis"], ["importacao", "pendencias"])

    def test_ca02_senha_errada_e_email_inexistente_tem_a_mesma_mensagem(self):
        senha_errada = self.entrar(senha="errada")
        email_inexistente = self.entrar(email="ninguem@genios.test")
        self.assertEqual(senha_errada.status_code, 401)
        self.assertEqual(email_inexistente.status_code, 401)
        self.assertEqual(senha_errada.json(), email_inexistente.json())
        self.assertEqual(senha_errada.json()["erro"]["mensagem"], "E-mail ou senha inválidos")

    def test_ca03_cinco_erros_bloqueiam_mesmo_com_a_senha_certa(self):
        for _ in range(5):
            self.entrar(senha="errada")
        resposta = self.entrar()
        self.assertEqual(resposta.status_code, 429)
        self.assertEqual(
            resposta.json()["erro"]["mensagem"], "Muitas tentativas. Tente novamente em 15 minutos"
        )

    def test_usuario_inativo_nao_entra(self):
        self.usuario.is_active = False
        self.usuario.save()
        self.assertEqual(self.entrar().status_code, 401)

    def test_campos_ausentes_respondem_400(self):
        resposta = self.cliente.post(URL_LOGIN, {"email": EMAIL}, format="json")
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.json()["erro"]["codigo"], "ENTRADA_INVALIDA")


class SessaoTest(TestCase):
    def setUp(self):
        self.polo = criar_polo("POLO_1")
        self.usuario = criar_usuario_com_perfil(EMAIL, Perfil.ALMOXARIFE, [self.polo])

    def test_me_devolve_o_usuario_do_token(self):
        resposta = cliente_autenticado(self.usuario).get(URL_ME)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["email"], EMAIL)
        self.assertCountEqual(resposta.json()["modulos"], ["almoxarifado", "equipes"])

    def test_ca06_sem_login_a_api_responde_401(self):
        for url in (URL_ME, "/api/v1/ordens-servico/", "/api/v1/almoxarifado/saidas-kits/"):
            resposta = APIClient().get(url)
            self.assertEqual(resposta.status_code, 401, url)
            self.assertEqual(resposta.json()["erro"]["codigo"], "NAO_AUTENTICADO")

    def test_ca05_logout_invalida_o_token_no_servidor(self):
        cliente = cliente_autenticado(self.usuario)
        self.assertEqual(cliente.post(URL_LOGOUT).status_code, 204)
        self.assertEqual(cliente.get(URL_ME).status_code, 401)

    def test_token_com_mais_de_8_horas_expira(self):
        cliente = cliente_autenticado(self.usuario)
        depois_do_turno = timezone.now() + timedelta(hours=8, minutes=1)
        with mock.patch("nucleo.autenticacao.timezone.now", return_value=depois_do_turno):
            resposta = cliente.get(URL_ME)
        self.assertEqual(resposta.status_code, 401)
        self.assertEqual(resposta.json()["erro"]["codigo"], "SESSAO_INVALIDA")

    def test_novo_login_troca_token_expirado(self):
        antigo = Token.objects.create(user=self.usuario)
        Token.objects.filter(pk=antigo.pk).update(created=timezone.now() - timedelta(hours=9))
        resposta = APIClient().post(
            URL_LOGIN, {"email": EMAIL, "senha": SENHA_TESTE}, format="json"
        )
        self.assertNotEqual(resposta.json()["access_token"], antigo.key)
