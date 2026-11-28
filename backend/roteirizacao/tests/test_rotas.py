"""HU-011 (operação e data), HU-012 (OSs no mapa) e HU-056 (criar rota) — contrato §7."""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from nucleo.models import EstadoOS, RegistroAuditoria
from roteirizacao.models import ItemRota, Rota
from roteirizacao.tests import cenario
from roteirizacao.tests.cenario import URL_PLANEJAMENTO, URL_ROTAS


class PainelDoPlanejamentoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cenario.montar(cls)
        cls.aptas = cenario.criar_aptas(cls.unidade, 3)
        cenario.criar_aptas(cls.unidade_sem_coordenada, 1, prefixo="8")

    def _painel(self, **params):
        return cenario.cliente(self).get(URL_PLANEJAMENTO, {**cenario.chave(self), **params})

    def test_hu011_ca01_mostra_operacao_data_e_ordens_aptas(self):
        corpo = self._painel().json()
        self.assertEqual(corpo["operacao"]["nome"], "PSS")
        self.assertEqual(corpo["data"], cenario.amanha().isoformat())
        self.assertEqual(len(corpo["ordens_aptas"]), 3)
        self.assertFalse(corpo["planejamento"]["somente_leitura"])

    def test_hu011_ca02_data_passada_e_somente_leitura(self):
        ontem = (timezone.localdate() - timedelta(days=1)).isoformat()
        planejamento = self._painel(data=ontem).json()["planejamento"]
        self.assertTrue(planejamento["somente_leitura"])
        self.assertEqual(
            planejamento["motivo_somente_leitura"],
            "Planejamento de data passada é somente leitura",
        )

    def test_hu011_ca03_sem_operacao_pede_para_escolher(self):
        resposta = cenario.cliente(self).get(URL_PLANEJAMENTO, {"data": "2030-01-01"})
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("Escolha a operação", str(resposta.json()))

    def test_hu012_ca03_os_inapta_nao_aparece_no_mapa(self):
        numeros = {ordem["numero"] for ordem in self._painel().json()["ordens_aptas"]}
        self.assertEqual(numeros, {ordem.numero for ordem in self.aptas})

    def test_hu012_ca08_polo_todos_exige_polo(self):
        resposta = cenario.cliente_autenticado_todos(self).get(
            URL_PLANEJAMENTO, cenario.chave(self)
        )
        self.assertEqual(resposta.status_code, 400)


class CriarRotaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cenario.montar(cls)

    def _criar(self, ordens, **campos):
        corpo = cenario.pedido_rota(self, ordens, **campos)
        return cenario.cliente(self).post(URL_ROTAS, corpo, format="json")

    def test_ca01_cria_rota_e_ordens_passam_a_roteirizada(self):
        ordens = cenario.criar_aptas(self.unidade, 18)
        resposta = self._criar(ordens)
        self.assertEqual(resposta.status_code, 201, resposta.content)
        self.assertEqual(len(resposta.json()["ordens"]), 18)
        for ordem in ordens:
            ordem.refresh_from_db()
            self.assertEqual(ordem.estado, EstadoOS.ROTEIRIZADA)

    def test_ca02_sem_previsao_de_inicio_nada_e_gravado(self):
        ordens = cenario.criar_aptas(self.unidade, 2)
        corpo = cenario.pedido_rota(self, ordens)
        del corpo["previsao_inicio"]
        resposta = cenario.cliente(self).post(URL_ROTAS, corpo, format="json")
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("Informe a previsão de início", str(resposta.json()))
        self.assertFalse(Rota.objects.exists())

    def test_ca03_equipe_de_outro_polo_da_422(self):
        ordens = cenario.criar_aptas(self.unidade, 2)
        resposta = self._criar(ordens, equipe_id=self.equipe_norte.pk)
        self.assertEqual(resposta.status_code, 422)

    def test_ca03_equipe_inativa_da_422(self):
        self.equipe_a.ativa = False
        self.equipe_a.save()
        resposta = self._criar(cenario.criar_aptas(self.unidade, 1))
        self.assertEqual(resposta.status_code, 422)

    def test_ca04_capacidade_do_dia_excedida(self):
        self.assertEqual(self._criar(cenario.criar_aptas(self.unidade, 10, "1")).status_code, 201)
        resposta = self._criar(cenario.criar_aptas(self.unidade, 18, "2"), nome="Tarde")
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(
            resposta.json()["erro"]["mensagem"],
            "Equipe EQ-A: 28 OSs no dia excede a capacidade de 25",
        )

    def test_ca05_os_ja_em_outra_rota(self):
        ordens = cenario.criar_aptas(self.unidade, 2)
        self._criar(ordens[:1])
        resposta = self._criar(ordens, nome="Outra")
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(
            resposta.json()["erro"]["mensagem"],
            f"OS {ordens[0].numero} já está na rota Bessa manhã",
        )
        self.assertEqual(ItemRota.objects.count(), 1)

    def test_ca06_data_passada_e_recusada(self):
        ontem = (timezone.localdate() - timedelta(days=1)).isoformat()
        resposta = self._criar(cenario.criar_aptas(self.unidade, 1), data=ontem)
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(
            resposta.json()["erro"]["mensagem"], "A data da rota não pode ser anterior a hoje"
        )

    def test_ca07_trilha_registra_rota_e_ordens(self):
        ordens = cenario.criar_aptas(self.unidade, 2)
        rota_id = self._criar(ordens).json()["id"]
        registro = RegistroAuditoria.objects.get(entidade="Rota", entidade_id=rota_id)
        self.assertEqual(registro.autor, self.coordenador)
        self.assertEqual(registro.valor_novo["ordens_ids"], [ordem.pk for ordem in ordens])

    def test_rn08_os_pendente_nao_entra_e_nada_e_gravado(self):
        apta = cenario.criar_aptas(self.unidade, 1)[0]
        pendente = cenario.criar_os(self.unidade, "PEND-1")
        resposta = self._criar([apta, pendente])
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(resposta.json()["erro"]["codigo"], "OS_INAPTA_PARA_ROTA")
        apta.refresh_from_db()
        self.assertEqual(apta.estado, EstadoOS.APTA_A_ROTEIRIZAR)
        self.assertFalse(Rota.objects.exists())
