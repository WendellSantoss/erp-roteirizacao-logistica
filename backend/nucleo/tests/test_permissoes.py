"""HU-020 — matriz de acesso por perfil e filtro global de polo (contrato §1)."""

from django.test import TestCase

from nucleo.models import Perfil
from nucleo.permissoes import MATRIZ_ACESSO, pode_acessar
from nucleo.tests.fabricas import cliente_autenticado, criar_polo, criar_usuario_com_perfil

# Uma rota de leitura e uma de escrita por módulo do MVP.
ROTAS = {
    "importacao": ("/api/v1/importacoes/", "/api/v1/importacoes/"),
    "pendencias": ("/api/v1/ordens-servico/", "/api/v1/ordens-servico/1/desconsiderar/"),
    "almoxarifado": ("/api/v1/almoxarifado/saidas-kits/", "/api/v1/almoxarifado/saidas-kits/"),
    "auditoria": ("/api/v1/auditoria/", None),
    "equipes": ("/api/v1/equipes/", None),
    "webscraper": ("/api/v1/unidades/", "/api/v1/unidades/1/coordenada/"),
    "roteirizador": ("/api/v1/roteirizacao/operacoes/", "/api/v1/roteirizacao/rotas/"),
}


class MatrizDeAcessoTest(TestCase):
    """CA03: um teste para cada célula "—" e para cada ação de escrita negada, verificando 403."""

    @classmethod
    def setUpTestData(cls):
        cls.polo = criar_polo("POLO_1")
        cls.clientes = {}
        for perfil in Perfil.values:
            usuario = criar_usuario_com_perfil(f"{perfil.lower()}@genios.test", perfil, [cls.polo])
            cls.clientes[perfil] = usuario

    def test_ca03_perfil_sem_acesso_recebe_403_na_leitura(self):
        for modulo, (rota_leitura, _) in ROTAS.items():
            for perfil, usuario in self.clientes.items():
                if pode_acessar(perfil, modulo, escrita=False):
                    continue
                with self.subTest(modulo=modulo, perfil=perfil):
                    resposta = cliente_autenticado(usuario, self.polo.pk).get(rota_leitura)
                    self.assertEqual(resposta.status_code, 403)

    def test_ca03_perfil_que_so_ve_recebe_403_na_escrita(self):
        for modulo, (_, rota_escrita) in ROTAS.items():
            if rota_escrita is None:
                continue
            for perfil, usuario in self.clientes.items():
                if pode_acessar(perfil, modulo, escrita=True):
                    continue
                with self.subTest(modulo=modulo, perfil=perfil):
                    resposta = cliente_autenticado(usuario, self.polo.pk).post(rota_escrita, {})
                    self.assertEqual(resposta.status_code, 403)

    def test_ca01_almoxarife_ve_so_almoxarifado_e_equipes(self):
        almoxarife = self.clientes[Perfil.ALMOXARIFE]
        modulos = cliente_autenticado(almoxarife).get("/api/v1/auth/me/").json()["modulos"]
        self.assertCountEqual(modulos, ["almoxarifado", "equipes"])

    def test_matriz_cobre_todos_os_modulos_do_mvp(self):
        self.assertEqual(set(MATRIZ_ACESSO), set(ROTAS))


class FiltroDePoloTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.polo_1, cls.polo_2 = criar_polo("POLO_1"), criar_polo("POLO_2")
        cls.analista = criar_usuario_com_perfil(
            "bruno@genios.test", Perfil.ANALISTA_OPERACOES, [cls.polo_2]
        )

    def test_escrita_com_polo_todos_responde_400(self):
        cliente = cliente_autenticado(self.analista, "TODOS")
        resposta = cliente.post("/api/v1/ordens-servico/1/desconsiderar/", {"justificativa": "x"})
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.json()["erro"]["codigo"], "POLO_OBRIGATORIO")

    def test_polo_nao_autorizado_responde_403(self):
        resposta = cliente_autenticado(self.analista, self.polo_1.pk).get("/api/v1/ordens-servico/")
        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(resposta.json()["erro"]["codigo"], "POLO_NAO_AUTORIZADO")

    def test_cabecalho_invalido_responde_400(self):
        resposta = cliente_autenticado(self.analista, "abc").get("/api/v1/ordens-servico/")
        self.assertEqual(resposta.status_code, 400)
