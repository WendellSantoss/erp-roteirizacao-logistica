"""HU-024 (coordenada manual) e HU-060 (liberar OSs para roteirização) — contrato §3 e §5."""

from decimal import Decimal

from django.test import TestCase

from nucleo.models import EstadoOS, Perfil, RegistroAuditoria
from nucleo.tests.fabricas import (
    cliente_autenticado,
    criar_os,
    criar_polo,
    criar_unidade,
    criar_usuario_com_perfil,
)

URL_LIBERAR = "/api/v1/ordens-servico/liberar/"


def url_coordenada(unidade_id: int) -> str:
    return f"/api/v1/unidades/{unidade_id}/coordenada/"


class CoordenadaManualTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.polo, cls.outro_polo = criar_polo("POLO_1"), criar_polo("POLO_2")
        cls.bessa = criar_unidade(cls.polo, "UN-BESSA")
        cls.unidade_norte = criar_unidade(cls.outro_polo, "UN-NORTE")
        cls.analista = criar_usuario_com_perfil(
            "ana@genios.test", Perfil.ANALISTA_OPERACOES, [cls.polo, cls.outro_polo]
        )

    def _salvar(self, latitude, longitude, unidade=None):
        cliente = cliente_autenticado(self.analista, self.polo.pk)
        corpo = {"latitude": latitude, "longitude": longitude}
        return cliente.patch(url_coordenada((unidade or self.bessa).pk), corpo, format="json")

    def test_ca01_digitar_coordenada_marca_como_manual(self):
        resposta = self._salvar("-7.0832", "-34.8336")
        self.assertEqual(resposta.status_code, 200, resposta.content)
        self.bessa.refresh_from_db()
        self.assertEqual(self.bessa.latitude, Decimal("-7.083200"))
        self.assertTrue(self.bessa.coordenada_manual)

    def test_ca01_unidade_sai_da_lista_sem_coordenada(self):
        self._salvar("-7.0832", "-34.8336")
        cliente = cliente_autenticado(self.analista, self.polo.pk)
        resposta = cliente.get("/api/v1/unidades/", {"sem_coordenada": "true"})
        self.assertEqual(resposta.json()["resultados"], [])

    def test_ca03_fora_da_area_e_recusada_e_nada_e_gravado(self):
        resposta = self._salvar("-23.5", "-46.6")
        self.assertEqual(resposta.status_code, 422)
        erro = resposta.json()["erro"]
        self.assertEqual(erro["mensagem"], "Coordenada fora da área de operação (Paraíba)")
        self.bessa.refresh_from_db()
        self.assertIsNone(self.bessa.latitude)

    def test_ca04_aceita_virgula_e_ponto(self):
        self.assertEqual(self._salvar("-7,0832", "-34,8336").status_code, 200)
        self.assertEqual(self._salvar(-7.0833, -34.8337).status_code, 200)
        self.bessa.refresh_from_db()
        self.assertEqual(self.bessa.longitude, Decimal("-34.833700"))

    def test_texto_invalido_da_400(self):
        self.assertEqual(self._salvar("abc", "-34.8").status_code, 400)

    def test_rn_l03_trilha_guarda_anterior_e_novo(self):
        self._salvar("-7.0832", "-34.8336")
        registro = RegistroAuditoria.objects.get(entidade="Unidade", entidade_id=self.bessa.pk)
        self.assertIsNone(registro.valor_anterior)
        self.assertEqual(registro.valor_novo, {"latitude": "-7.083200", "longitude": "-34.833600"})
        self.assertEqual(registro.autor, self.analista)

    def test_unidade_de_outro_polo_da_403(self):
        resposta = self._salvar("-7.0832", "-34.8336", unidade=self.unidade_norte)
        self.assertEqual(resposta.status_code, 403)


class LiberarParaRoteirizacaoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.polo = criar_polo("POLO_1")
        cls.com_coordenada = criar_unidade(cls.polo, "UN-01", com_coordenada=True)
        cls.sem_coordenada = criar_unidade(cls.polo, "UN-02")
        cls.analista = criar_usuario_com_perfil(
            "ana@genios.test", Perfil.ANALISTA_OPERACOES, [cls.polo]
        )

    def _liberar(self, ordens):
        cliente = cliente_autenticado(self.analista, self.polo.pk)
        corpo = {"ordens_ids": [ordem.pk for ordem in ordens]}
        return cliente.post(URL_LIBERAR, corpo, format="json")

    def test_ca01_liberar_em_lote(self):
        ordens = [criar_os(self.com_coordenada, f"10{i}") for i in range(3)]
        resposta = self._liberar(ordens)
        self.assertEqual(resposta.status_code, 200, resposta.content)
        self.assertEqual(len(resposta.json()["liberadas"]), 3)
        for ordem in ordens:
            ordem.refresh_from_db()
            self.assertEqual(ordem.estado, EstadoOS.APTA_A_ROTEIRIZAR)

    def test_ca02_os_sem_coordenada_e_pulada_e_informada(self):
        apta = criar_os(self.com_coordenada, "201")
        sem_coordenada = criar_os(self.sem_coordenada, "202")
        corpo = self._liberar([apta, sem_coordenada]).json()
        self.assertEqual(corpo["liberadas"], ["201"])
        self.assertEqual(corpo["nao_liberadas"], [{"numero": "202", "motivo": "sem coordenada"}])
        sem_coordenada.refresh_from_db()
        self.assertEqual(sem_coordenada.estado, EstadoOS.PENDENTE)

    def test_ca03_cada_os_liberada_tem_transicao_na_trilha(self):
        ordem = criar_os(self.com_coordenada, "301")
        self._liberar([ordem])
        registro = RegistroAuditoria.objects.get(entidade="OrdemServico", entidade_id=ordem.pk)
        self.assertEqual(registro.valor_novo, EstadoOS.APTA_A_ROTEIRIZAR)
        self.assertEqual(registro.autor, self.analista)

    def test_polo_todos_exige_polo_especifico(self):
        ordem = criar_os(self.com_coordenada, "401")
        cliente = cliente_autenticado(self.analista, "TODOS")
        resposta = cliente.post(URL_LIBERAR, {"ordens_ids": [ordem.pk]}, format="json")
        self.assertEqual(resposta.status_code, 400)

    def test_lista_vazia_da_400(self):
        self.assertEqual(self._liberar([]).status_code, 400)
