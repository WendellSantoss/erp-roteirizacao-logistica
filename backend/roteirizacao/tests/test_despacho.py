"""HU-013 (finalizar planejamento) e HU-014 (arquivo RPA) — contrato §7."""

from django.test import TestCase

from nucleo.models import EstadoOS, RegistroAuditoria
from roteirizacao.arquivo_rpa import COLUNAS
from roteirizacao.models import ArquivoDespacho, Planejamento, StatusPlanejamento
from roteirizacao.tests import cenario
from roteirizacao.tests.cenario import URL_FINALIZAR, URL_ROTAS, URL_RPA


class FinalizarPlanejamentoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cenario.montar(cls)

    def setUp(self):
        self.cliente = cenario.cliente(self)

    def _criar_rota(self, quantidade=3, nome="Bessa manhã", prefixo="9"):
        ordens = cenario.criar_aptas(self.unidade, quantidade, prefixo)
        corpo = cenario.pedido_rota(self, ordens, nome=nome)
        self.assertEqual(self.cliente.post(URL_ROTAS, corpo, format="json").status_code, 201)
        return ordens

    def _finalizar(self):
        return self.cliente.post(URL_FINALIZAR, cenario.chave(self), format="json")

    def test_ca01_finaliza_com_autor_e_data(self):
        self._criar_rota()
        resposta = self._finalizar()
        self.assertEqual(resposta.status_code, 200, resposta.content)
        planejamento = Planejamento.objects.get()
        self.assertEqual(planejamento.status, StatusPlanejamento.FINALIZADO)
        self.assertEqual(planejamento.finalizado_por, self.coordenador)
        self.assertIsNotNone(planejamento.finalizado_em)

    def test_ca02_equipe_inativada_bloqueia_e_lista_inconsistencia(self):
        self._criar_rota()
        self.equipe_a.ativa = False
        self.equipe_a.save()
        resposta = self._finalizar()
        self.assertEqual(resposta.status_code, 422)
        inconsistencias = resposta.json()["erro"]["detalhes"]["inconsistencias"]
        self.assertEqual(inconsistencias[0]["rota"], "Bessa manhã")
        self.assertIn("inativada", inconsistencias[0]["motivo"])
        self.assertEqual(Planejamento.objects.get().status, StatusPlanejamento.ABERTO)

    def test_ca02_os_desconsiderada_no_caminho_bloqueia(self):
        ordem = self._criar_rota(quantidade=1)[0]
        ordem.estado = EstadoOS.DESCONSIDERADA  # simula dado corrompido fora do fluxo normal
        ordem.save(update_fields=["estado"])
        resposta = self._finalizar()
        self.assertEqual(resposta.status_code, 422)
        self.assertIn(ordem.numero, str(resposta.json()["erro"]["detalhes"]))

    def test_ca03_planejamento_finalizado_nao_aceita_nova_rota(self):
        self._criar_rota()
        self._finalizar()
        ordens = cenario.criar_aptas(self.unidade, 1, prefixo="7")
        corpo = cenario.pedido_rota(self, ordens, nome="Tarde")
        resposta = self.cliente.post(URL_ROTAS, corpo, format="json")
        self.assertEqual(resposta.status_code, 409)
        self.assertEqual(resposta.json()["erro"]["mensagem"], "Planejamento finalizado")

    def test_ca04_sem_rotas(self):
        resposta = self._finalizar()
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(resposta.json()["erro"]["mensagem"], "Não há rotas para finalizar")


class ArquivoRpaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cenario.montar(cls)

    def setUp(self):
        self.cliente = cenario.cliente(self)
        self.ordens = cenario.criar_aptas(self.unidade, 4)
        corpo = cenario.pedido_rota(self, self.ordens)
        self.cliente.post(URL_ROTAS, corpo, format="json")

    def _gerar(self):
        return self.cliente.post(URL_RPA, cenario.chave(self), format="json")

    def test_ca02_planejamento_aberto_da_422(self):
        resposta = self._gerar()
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(
            resposta.json()["erro"]["mensagem"], "Finalize o planejamento antes de gerar o RPA"
        )

    def test_ca01_gera_arquivo_e_despacha_as_ordens(self):
        self.cliente.post(URL_FINALIZAR, cenario.chave(self), format="json")
        resposta = self._gerar()
        self.assertEqual(resposta.status_code, 201, resposta.content)
        self.assertEqual(resposta.json()["total_ordens"], 4)
        for ordem in self.ordens:
            ordem.refresh_from_db()
            self.assertEqual(ordem.estado, EstadoOS.DESPACHADA)
        self.assertEqual(Planejamento.objects.get().status, StatusPlanejamento.DESPACHADO)

    def test_ca03_arquivo_rastreavel_com_hash_e_ordens(self):
        self.cliente.post(URL_FINALIZAR, cenario.chave(self), format="json")
        corpo = self._gerar().json()
        arquivo = ArquivoDespacho.objects.get()
        self.assertEqual(corpo["hash_sha256"], arquivo.hash_sha256)
        self.assertEqual(len(arquivo.hash_sha256), 64)
        for ordem in self.ordens:
            self.assertIn(ordem.numero, arquivo.conteudo)

    def test_ca04_baixar_de_novo_devolve_o_mesmo_arquivo(self):
        self.cliente.post(URL_FINALIZAR, cenario.chave(self), format="json")
        primeiro = self._gerar().json()
        segundo = self._gerar()
        self.assertEqual(segundo.status_code, 200)
        self.assertEqual(segundo.json()["hash_sha256"], primeiro["hash_sha256"])
        download = self.cliente.get(URL_RPA, cenario.chave(self))
        self.assertEqual(download["X-Hash-Sha256"], primeiro["hash_sha256"])
        self.assertEqual(ArquivoDespacho.objects.count(), 1)

    def test_ca06_layout_cabecalho_separador_e_linhas(self):
        self.cliente.post(URL_FINALIZAR, cenario.chave(self), format="json")
        self._gerar()
        linhas = ArquivoDespacho.objects.get().conteudo.split("\r\n")
        self.assertEqual(linhas[0], ";".join(COLUNAS))
        self.assertTrue(linhas[1].startswith(f"{self.ordens[0].numero};POLO_1;PSS;"))
        self.assertEqual(len([linha for linha in linhas if linha]), 1 + len(self.ordens))

    def test_rnf17_geracao_fica_na_trilha(self):
        self.cliente.post(URL_FINALIZAR, cenario.chave(self), format="json")
        self._gerar()
        valores = RegistroAuditoria.objects.filter(entidade="Planejamento").values_list(
            "valor_novo", flat=True
        )
        self.assertIn(StatusPlanejamento.DESPACHADO, list(valores))
