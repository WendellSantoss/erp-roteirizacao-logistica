"""HU-006/007/008 — listagem de pendências, atraso, prioridade e desconsideração (contrato §5)."""

from datetime import datetime, timedelta

from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from nucleo.models import EstadoOS, OrdemServico, Perfil, RegistroAuditoria
from nucleo.services import calcular_prazos
from nucleo.tests.fabricas import (
    cliente_autenticado,
    criar_os,
    criar_polo,
    criar_unidade,
    criar_usuario_com_perfil,
)

URL = "/api/v1/ordens-servico/"
FUSO = timezone.get_fixed_timezone(-180)


class CalculoDeAtrasoTest(SimpleTestCase):
    """HU-008 RN-06: atraso = (agora − abertura) − prazo."""

    def test_ca01_em_atraso(self):
        prazos = calcular_prazos(
            datetime(2026, 7, 10, 8, tzinfo=FUSO), 24, datetime(2026, 7, 11, 14, tzinfo=FUSO)
        )
        self.assertEqual((prazos.tempo_decorrido_horas, prazos.atraso_horas), (30.0, 6.0))
        self.assertTrue(prazos.em_atraso)

    def test_ca02_exatamente_no_limite_nao_esta_atrasada(self):
        prazos = calcular_prazos(
            datetime(2026, 7, 10, 14, tzinfo=FUSO), 24, datetime(2026, 7, 11, 14, tzinfo=FUSO)
        )
        self.assertEqual(prazos.atraso_horas, 0)
        self.assertFalse(prazos.em_atraso)

    def test_ca03_no_prazo(self):
        prazos = calcular_prazos(
            datetime(2026, 7, 11, 8, tzinfo=FUSO), 48, datetime(2026, 7, 11, 14, tzinfo=FUSO)
        )
        self.assertEqual(prazos.tempo_decorrido_horas, 6.0)
        self.assertFalse(prazos.em_atraso)


class ListagemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.polo_1, cls.polo_2 = criar_polo("POLO_1"), criar_polo("POLO_2")
        unidade_1, unidade_2 = criar_unidade(cls.polo_1), criar_unidade(cls.polo_2)
        cls.analista = criar_usuario_com_perfil(
            "ana@genios.test", Perfil.ANALISTA_OPERACOES, [cls.polo_1, cls.polo_2]
        )
        agora = timezone.now()
        cls.no_prazo = _os(unidade_1, "1", agora - timedelta(hours=2))
        cls.atrasada = _os(unidade_1, "2", agora - timedelta(hours=50))
        cls.prioritaria = _os(unidade_1, "3", agora - timedelta(hours=1), prioridade=True)
        _os(unidade_1, "4", agora, estado=EstadoOS.ROTEIRIZADA)
        _os(unidade_2, "5", agora)

    def listar(self, polo="TODOS", **filtros):
        return cliente_autenticado(self.analista, polo).get(URL, filtros).json()

    def test_ca01_lista_pendentes_do_polo_ordenadas_por_prioridade_e_atraso(self):
        corpo = self.listar(self.polo_1.pk)
        self.assertEqual(corpo["total"], 3)
        numeros = [ordem["numero"] for ordem in corpo["resultados"]]
        self.assertEqual(numeros, ["3", "2", "1"])
        self.assertEqual(corpo["contadores_por_status"], {"PENDENTE": 3, "ROTEIRIZADA": 1})

    def test_ca05_todos_traz_os_polos_do_usuario_com_o_polo(self):
        corpo = self.listar("TODOS")
        self.assertEqual(corpo["total"], 4)
        self.assertIn("polo", corpo["resultados"][0])

    def test_resultado_traz_colunas_e_atraso_calculado(self):
        ordem = next(o for o in self.listar(self.polo_1.pk)["resultados"] if o["numero"] == "2")
        self.assertTrue(ordem["em_atraso"])
        self.assertAlmostEqual(ordem["atraso_horas"], 26, delta=0.1)
        for coluna in ("especificacao", "numero_imovel", "cidade", "setor", "quadra", "unidade"):
            self.assertIn(coluna, ordem)

    def test_filtro_atrasada_e_busca(self):
        self.assertEqual(self.listar(self.polo_1.pk, atrasada="true")["total"], 1)
        self.assertEqual(self.listar(self.polo_1.pk, busca="3")["total"], 1)

    def test_paginacao_respeita_page_size(self):
        corpo = self.listar(self.polo_1.pk, page_size=2, page=2)
        self.assertEqual(corpo["total"], 3)
        self.assertEqual(len(corpo["resultados"]), 1)

    def test_page_size_acima_do_maximo_responde_400(self):
        resposta = cliente_autenticado(self.analista).get(URL, {"page_size": 500})
        self.assertEqual(resposta.status_code, 400)

    def test_ca04_lista_vazia(self):
        self.assertEqual(self.listar(self.polo_2.pk, estado="VALIDADA")["resultados"], [])


class TratamentoTest(TestCase):
    def setUp(self):
        self.polo_1, self.polo_2 = criar_polo("POLO_1"), criar_polo("POLO_2")
        self.analista = criar_usuario_com_perfil(
            "ana@genios.test", Perfil.ANALISTA_OPERACOES, [self.polo_1, self.polo_2]
        )
        self.ordem = criar_os(criar_unidade(self.polo_1))
        self.cliente = cliente_autenticado(self.analista, self.polo_1.pk)

    def url(self, acao: str, ordem_id: int | None = None) -> str:
        return f"{URL}{ordem_id or self.ordem.pk}/{acao}/"

    def test_marcar_prioridade_grava_auditoria_com_justificativa_padrao(self):
        resposta = self.cliente.patch(self.url("prioridade"), {"prioridade": True}, format="json")
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.json()["prioridade"])
        registro = RegistroAuditoria.objects.get(campo="prioridade")
        self.assertEqual(registro.justificativa, "Alteração manual de prioridade")
        self.assertEqual((registro.valor_anterior, registro.valor_novo), (False, True))

    def test_prioridade_sem_campo_responde_400(self):
        resposta = self.cliente.patch(self.url("prioridade"), {}, format="json")
        self.assertEqual(resposta.status_code, 400)

    def test_prioridade_em_os_desconsiderada_responde_409(self):
        OrdemServico.objects.filter(pk=self.ordem.pk).update(estado=EstadoOS.DESCONSIDERADA)
        resposta = self.cliente.patch(self.url("prioridade"), {"prioridade": True}, format="json")
        self.assertEqual(resposta.status_code, 409)

    def test_os_de_outro_polo_responde_403_e_inexistente_404(self):
        cliente_polo_2 = cliente_autenticado(self.analista, self.polo_2.pk)
        corpo = {"prioridade": True}
        resposta = cliente_polo_2.patch(self.url("prioridade"), corpo, format="json")
        self.assertEqual(resposta.status_code, 403)
        resposta = self.cliente.patch(self.url("prioridade", 999999), corpo, format="json")
        self.assertEqual(resposta.status_code, 404)

    def test_desconsiderar_muda_estado_e_registra_justificativa(self):
        corpo = {"justificativa": "OS em duplicidade (teste)."}
        resposta = self.cliente.post(self.url("desconsiderar"), corpo, format="json")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["estado"], EstadoOS.DESCONSIDERADA)
        self.assertTrue(resposta.json()["auditoria_registrada"])
        registro = RegistroAuditoria.objects.get(campo="estado")
        self.assertEqual(registro.justificativa, "OS em duplicidade (teste).")

    def test_desconsiderar_sem_justificativa_responde_400(self):
        resposta = self.cliente.post(self.url("desconsiderar"), {"justificativa": " "})
        self.assertEqual(resposta.status_code, 400)

    def test_desconsiderar_os_executada_responde_409(self):
        OrdemServico.objects.filter(pk=self.ordem.pk).update(estado=EstadoOS.EXECUTADA)
        resposta = self.cliente.post(self.url("desconsiderar"), {"justificativa": "x"})
        self.assertEqual(resposta.status_code, 409)
        self.assertEqual(resposta.json()["erro"]["codigo"], "TRANSICAO_NAO_PERMITIDA")

    def test_trilha_de_auditoria_lista_o_que_foi_feito(self):
        self.cliente.post(self.url("desconsiderar"), {"justificativa": "teste"})
        gerente = criar_usuario_com_perfil("g@genios.test", Perfil.GERENTE_CONTRATO, [self.polo_1])
        resposta = cliente_autenticado(gerente).get(
            "/api/v1/auditoria/", {"entidade": "OrdemServico", "entidade_id": self.ordem.pk}
        )
        self.assertEqual(resposta.status_code, 200)
        registro = resposta.json()["resultados"][0]
        self.assertEqual(registro["valor_novo"], EstadoOS.DESCONSIDERADA)
        self.assertEqual(registro["autor"], "Usuária Teste")


def _os(unidade, numero, abertura, **alteracoes):
    ordem = criar_os(unidade, numero)
    OrdemServico.objects.filter(pk=ordem.pk).update(abertura=abertura, **alteracoes)
    return ordem
