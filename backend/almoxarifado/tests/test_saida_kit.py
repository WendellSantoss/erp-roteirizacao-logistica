"""HU-016 — trava de histórico na saída de kits (contrato §6)."""

import threading
from datetime import timedelta

from django.db import connection
from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from almoxarifado.excecoes import TravaHistoricoExcedida
from almoxarifado.models import ExecucaoKit, SaidaKit, TipoKit
from almoxarifado.services import PedidoSaida, registrar_saida_kit
from nucleo.models import Perfil, RegistroAuditoria
from nucleo.tests.fabricas import (
    cliente_autenticado,
    criar_equipe,
    criar_polo,
    criar_usuario_com_perfil,
)

URL_SAIDAS = "/api/v1/almoxarifado/saidas-kits/"
URL_LIMITES = "/api/v1/almoxarifado/limites-kits/"


def montar_cenario(caso):
    """Polo 1 com 10 Kit Hidrômetro executados ontem; Polo 2 sem execução (CA01/CA05)."""
    caso.polo_1, caso.polo_2 = criar_polo("POLO_1"), criar_polo("POLO_2")
    caso.kit = TipoKit.objects.create(codigo="KIT_HIDROMETRO", nome="Kit Hidrômetro")
    caso.supressao = TipoKit.objects.create(codigo="KIT_SUPRESSAO", nome="Kit Supressão")
    ontem = timezone.localdate() - timedelta(days=1)
    ExecucaoKit.objects.create(polo=caso.polo_1, tipo_kit=caso.kit, data=ontem, quantidade=10)
    caso.equipe_a = criar_equipe(caso.polo_1, "EQ-A")
    caso.equipe_b = criar_equipe(caso.polo_1, "EQ-B")
    caso.equipe_norte = criar_equipe(caso.polo_2, "EQ-N")
    caso.almoxarife = criar_usuario_com_perfil(
        "carlos@genios.test", Perfil.ALMOXARIFE, [caso.polo_1, caso.polo_2]
    )


class TravaDeHistoricoTest(TestCase):
    def setUp(self):
        montar_cenario(self)
        self.cliente = cliente_autenticado(self.almoxarife, self.polo_1.pk)

    def sair(self, quantidade, equipe=None, kit=None, cliente=None):
        corpo = {
            "equipe_id": (equipe or self.equipe_a).pk,
            "kit_id": (kit or self.kit).pk,
            "quantidade": quantidade,
        }
        return (cliente or self.cliente).post(URL_SAIDAS, corpo, format="json")

    def limite_do_kit(self) -> dict:
        kits = self.cliente.get(URL_LIMITES).json()["kits"]
        return next(k for k in kits if k["tipo_kit"] == "KIT_HIDROMETRO")

    def test_ca01_dentro_do_limite_registra_e_zera_o_saldo(self):
        resposta = self.sair(10)
        self.assertEqual(resposta.status_code, 201, resposta.content)
        self.assertEqual(resposta.json()["tipo_kit"], "KIT_HIDROMETRO")
        self.assertEqual(self.limite_do_kit()["saldo_disponivel_hoje"], 0)

    def test_ca02_acima_do_limite_bloqueia_com_a_mensagem_do_rf_alm_04(self):
        self.sair(10)
        resposta = self.sair(1, self.equipe_b)
        self.assertEqual(resposta.status_code, 422)
        erro = resposta.json()["erro"]
        self.assertEqual(erro["codigo"], "TRAVA_HISTORICO_KIT_EXCEDIDA")
        self.assertIn(
            "Kit Hidrômetro · Solicitado hoje: 11 un. · Executado ontem: 10 un.", erro["mensagem"]
        )
        self.assertEqual(erro["detalhes"]["ja_retirado_hoje"], 10)
        self.assertEqual(SaidaKit.objects.count(), 1)

    def test_ca03_soma_do_dia(self):
        self.assertEqual(self.sair(6).status_code, 201)
        resposta = self.sair(5, self.equipe_b)
        self.assertEqual(resposta.status_code, 422)
        self.assertIn("Solicitado hoje: 11 un.", resposta.json()["erro"]["mensagem"])

    def test_ca04_sem_historico_o_limite_e_zero(self):
        resposta = self.sair(1, kit=self.supressao)
        self.assertEqual(resposta.status_code, 422)
        self.assertIn("Executado ontem: 0 un.", resposta.json()["erro"]["mensagem"])

    def test_ca05_limite_e_por_polo(self):
        cliente_norte = cliente_autenticado(self.almoxarife, self.polo_2.pk)
        resposta = self.sair(5, self.equipe_norte, cliente=cliente_norte)
        self.assertEqual(resposta.status_code, 422)

    def test_ca06_contorno_pela_api_nao_grava(self):
        self.sair(10)
        self.assertEqual(self.sair(1).status_code, 422)
        self.assertEqual(SaidaKit.objects.count(), 1)

    def test_ca08_tentativa_bloqueada_fica_na_auditoria(self):
        self.sair(11)
        registro = RegistroAuditoria.objects.get(campo="tentativa_bloqueada")
        self.assertEqual(registro.autor, self.almoxarife)
        self.assertEqual(registro.polo, self.polo_1)
        self.assertEqual(registro.valor_novo["quantidade_solicitada"], 11)
        self.assertEqual(registro.valor_novo["limite_executado_ontem"], 10)

    def test_equipe_de_outro_polo_responde_403(self):
        self.assertEqual(self.sair(1, self.equipe_norte).status_code, 403)

    def test_quantidade_zero_e_polo_todos_respondem_400(self):
        self.assertEqual(self.sair(0).status_code, 400)
        cliente_todos = cliente_autenticado(self.almoxarife, "TODOS")
        self.assertEqual(self.sair(1, cliente=cliente_todos).status_code, 400)

    def test_kit_ou_equipe_inexistente_responde_404(self):
        corpo = {"equipe_id": 999999, "kit_id": self.kit.pk, "quantidade": 1}
        self.assertEqual(self.cliente.post(URL_SAIDAS, corpo, format="json").status_code, 404)

    def test_listagem_de_saidas_do_dia(self):
        self.sair(3)
        resultados = self.cliente.get(URL_SAIDAS).json()["resultados"]
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["equipe"], "EQ-A (Equipe de teste)")


class ConcorrenciaTest(TransactionTestCase):
    """CA07: duas saídas de 6 ao mesmo tempo com limite 10 → exatamente uma é aceita."""

    def setUp(self):
        montar_cenario(self)

    def test_ca07_duas_saidas_simultaneas_nao_passam_do_limite(self):
        largada = threading.Barrier(2)
        resultados = []

        def tentar(equipe):
            pedido = PedidoSaida(self.polo_1.pk, equipe.pk, self.kit.pk, 6)
            largada.wait()
            try:
                registrar_saida_kit(pedido, self.almoxarife)
                resultados.append("aceita")
            except TravaHistoricoExcedida:
                resultados.append("bloqueada")
            finally:
                connection.close()

        threads = [
            threading.Thread(target=tentar, args=(e,)) for e in (self.equipe_a, self.equipe_b)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertCountEqual(resultados, ["aceita", "bloqueada"])
        self.assertEqual(SaidaKit.objects.count(), 1)
