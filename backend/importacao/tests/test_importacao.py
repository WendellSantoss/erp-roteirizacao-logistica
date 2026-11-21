"""HU-001 a HU-004 — POST/GET /api/v1/importacoes/ (contrato §4)."""

from unittest import mock

from django.db import DatabaseError
from django.test import TestCase, override_settings

from importacao.models import Importacao, StatusImportacao
from importacao.tests.planilhas import CABECALHO, arquivo, linha_gsan, planilha_xlsx
from nucleo.models import EstadoOS, OrdemServico, Perfil
from nucleo.tests.fabricas import (
    cliente_autenticado,
    criar_equipe,
    criar_polo,
    criar_unidade,
    criar_usuario_com_perfil,
)

URL = "/api/v1/importacoes/"


class BaseImportacao(TestCase):
    def setUp(self):
        self.polo_1, self.polo_2 = criar_polo("POLO_1"), criar_polo("POLO_2")
        self.unidade = criar_unidade(self.polo_1, "UN-01")
        fora = criar_unidade(self.polo_1, "UN-09")
        fora.no_escopo = False
        fora.save()
        criar_unidade(self.polo_2, "UN-21")
        self.analista = criar_usuario_com_perfil(
            "ana@genios.test", Perfil.ANALISTA_OPERACOES, [self.polo_1, self.polo_2]
        )
        self.cliente = cliente_autenticado(self.analista, self.polo_1.pk)

    def importar(self, linhas, cliente=None, **opcoes):
        conteudo = planilha_xlsx(linhas, opcoes.get("cabecalho"))
        envio = {"arquivo": arquivo(conteudo, opcoes.get("nome", "gsan_os.xlsx"))}
        return (cliente or self.cliente).post(URL, envio, format="multipart")


class RecebimentoTest(BaseImportacao):
    """HU-001."""

    def test_ca01_envio_valido_registra_importacao_com_hash(self):
        resposta = self.importar([linha_gsan("100")])
        self.assertEqual(resposta.status_code, 201, resposta.content)
        corpo = resposta.json()
        self.assertEqual(corpo["status"], StatusImportacao.CONCLUIDA)
        self.assertEqual(len(corpo["hash_sha256"]), 64)
        importacao = Importacao.objects.get(pk=corpo["id"])
        self.assertEqual(
            (importacao.usuario, importacao.polo, importacao.nome_arquivo),
            (self.analista, self.polo_1, "gsan_os.xlsx"),
        )

    def test_ca03_extensao_invalida_e_recusada_sem_registrar(self):
        resposta = self.importar([linha_gsan("100")], nome="gsan.csv")
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(
            resposta.json()["erro"]["mensagem"],
            "Formato não aceito: envie a planilha do GSAN em .xlsx",
        )
        self.assertFalse(Importacao.objects.exists())

    @override_settings(LIMITE_PLANILHA_BYTES=1024)
    def test_ca04_ca05_arquivo_acima_do_limite_responde_413_sem_registrar(self):
        resposta = self.importar([linha_gsan(str(n)) for n in range(50)])
        self.assertEqual(resposta.status_code, 413)
        self.assertFalse(Importacao.objects.exists())

    def test_ca06_polo_todos_responde_400(self):
        cliente = cliente_autenticado(self.analista, "TODOS")
        self.assertEqual(self.importar([linha_gsan("1")], cliente).status_code, 400)

    def test_ca07_almoxarife_recebe_403(self):
        almoxarife = criar_usuario_com_perfil("c@genios.test", Perfil.ALMOXARIFE, [self.polo_1])
        cliente = cliente_autenticado(almoxarife, self.polo_1.pk)
        self.assertEqual(self.importar([linha_gsan("1")], cliente).status_code, 403)

    def test_ca08_mais_de_um_arquivo_responde_400(self):
        conteudo = planilha_xlsx([linha_gsan("1")])
        envio = {"arquivo": [arquivo(conteudo, "a.xlsx"), arquivo(conteudo, "b.xlsx")]}
        resposta = self.cliente.post(URL, envio, format="multipart")
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.json()["erro"]["mensagem"], "Envie um arquivo por vez")

    def test_sem_arquivo_responde_400(self):
        self.assertEqual(self.cliente.post(URL, {}, format="multipart").status_code, 400)

    def test_409_com_importacao_em_andamento_no_polo(self):
        Importacao.objects.create(
            polo=self.polo_1, usuario=self.analista, nome_arquivo="x.xlsx", hash_sha256="0" * 64
        )
        self.assertEqual(self.importar([linha_gsan("1")]).status_code, 409)


class LayoutTest(BaseImportacao):
    """HU-002."""

    def test_ca02_coluna_ausente_recusa_tudo_e_registra_recusada(self):
        cabecalho = [c for c in CABECALHO if c not in ("Setor", "Quadra")]
        resposta = self.importar([linha_gsan("1")], cabecalho=cabecalho)
        self.assertEqual(resposta.status_code, 422)
        erro = resposta.json()["erro"]
        self.assertEqual(erro["codigo"], "CABECALHO_PLANILHA_INVALIDO")
        self.assertEqual(erro["detalhes"]["colunas_faltantes"], ["Setor", "Quadra"])
        self.assertEqual(erro["mensagem"], "Colunas obrigatórias ausentes: Setor, Quadra")
        self.assertFalse(OrdemServico.objects.exists())
        self.assertEqual(Importacao.objects.get().status, StatusImportacao.RECUSADA)

    def test_ca03_linhas_invalidas_viram_alerta_e_o_resto_entra(self):
        linhas = [
            linha_gsan("1"),
            linha_gsan(""),
            linha_gsan("3", Abertura="31/02/2026"),
            linha_gsan("4", **{"Prazo (h)": -4}),
        ]
        corpo = self.importar(linhas).json()
        self.assertEqual(corpo["resumo"]["novas"], 1)
        self.assertEqual(
            [(a["linha"], a["campo"]) for a in corpo["alertas"]],
            [(3, "numero"), (4, "abertura"), (5, "prazo_horas")],
        )

    def test_ca04_os_repetida_no_arquivo_vale_a_primeira(self):
        corpo = self.importar([linha_gsan("7"), linha_gsan("7", Tipo="OUTRO")]).json()
        self.assertEqual(corpo["resumo"]["novas"], 1)
        self.assertEqual(corpo["alertas"][0]["motivo"], "OS 7 repetida na linha 3")
        self.assertEqual(OrdemServico.objects.get().tipo, "RELIGACAO_AGUA")

    def test_ca05_ordem_das_colunas_e_colunas_extras_nao_importam(self):
        cabecalho = ["Observação GSAN", *reversed(CABECALHO)]
        self.assertEqual(self.importar([linha_gsan("1")], cabecalho=cabecalho).status_code, 201)

    def test_ca06_arquivo_corrompido_e_recusado(self):
        envio = {"arquivo": arquivo(b"isto nao e um xlsx")}
        resposta = self.cliente.post(URL, envio, format="multipart")
        self.assertEqual(resposta.status_code, 422)
        self.assertEqual(resposta.json()["erro"]["codigo"], "PLANILHA_ILEGIVEL")

    def test_prazo_vazio_usa_padrao_com_alerta(self):
        corpo = self.importar([linha_gsan("1", **{"Prazo (h)": None})]).json()
        self.assertEqual(corpo["alertas"][0]["campo"], "prazo_horas")
        self.assertEqual(OrdemServico.objects.get().prazo_horas, 48)


class EscopoTest(BaseImportacao):
    """HU-003."""

    def test_ca01_ca02_fora_de_escopo_nao_grava_e_entra_no_resumo(self):
        linhas = [linha_gsan("1"), linha_gsan("2", "UN-09"), linha_gsan("3", "UN-09")]
        corpo = self.importar(linhas).json()
        self.assertEqual((corpo["resumo"]["novas"], corpo["resumo"]["fora_escopo"]), (1, 2))
        self.assertIn(
            "UN-09 fora do escopo do polo — 2 OSs ignoradas", corpo["alertas"][0]["motivo"]
        )

    def test_ca03_unidade_desconhecida_gera_alerta(self):
        corpo = self.importar([linha_gsan("1", "Jardim Novo")]).json()
        self.assertEqual(
            corpo["alertas"][0]["motivo"], "Unidade Jardim Novo não cadastrada — 1 OSs ignoradas"
        )

    def test_ca04_unidade_de_outro_polo_e_descartada(self):
        corpo = self.importar([linha_gsan("1", "UN-21")]).json()
        self.assertEqual(corpo["resumo"]["fora_escopo"], 1)
        self.assertFalse(OrdemServico.objects.exists())


class UpsertTest(BaseImportacao):
    """HU-004."""

    def ordem(self, numero="1", polo=None) -> OrdemServico:
        return OrdemServico.objects.get(numero=numero, polo=polo or self.polo_1)

    def test_ca01_novas_e_atualizadas(self):
        self.importar([linha_gsan("1"), linha_gsan("2")])
        corpo = self.importar([linha_gsan("1"), linha_gsan("2"), linha_gsan("3")]).json()
        self.assertEqual((corpo["resumo"]["novas"], corpo["resumo"]["atualizadas"]), (1, 2))
        self.assertEqual(self.ordem("3").estado, EstadoOS.PENDENTE)

    def test_ca02_tratamento_preservado_e_campo_gsan_atualizado(self):
        self.importar([linha_gsan("1")])
        equipe = criar_equipe(self.polo_1)
        OrdemServico.objects.filter(numero="1").update(prioridade=True, equipe=equipe)
        self.importar([linha_gsan("1", **{"Especificação": "Nova especificação"})])
        ordem = self.ordem()
        self.assertEqual((ordem.prioridade, ordem.equipe), (True, equipe))
        self.assertEqual(ordem.especificacao, "Nova especificação")

    def test_ca03_ca04_estado_nao_muda_na_reimportacao(self):
        self.importar([linha_gsan("1"), linha_gsan("2")])
        OrdemServico.objects.filter(numero="1").update(estado=EstadoOS.DESCONSIDERADA)
        OrdemServico.objects.filter(numero="2").update(estado=EstadoOS.ROTEIRIZADA)
        self.importar([linha_gsan("1"), linha_gsan("2", **{"Prazo (h)": 72})])
        self.assertEqual(self.ordem("1").estado, EstadoOS.DESCONSIDERADA)
        self.assertEqual((self.ordem("2").estado, self.ordem("2").prazo_horas), ("ROTEIRIZADA", 72))

    def test_ca05_os_ausente_na_planilha_nao_e_alterada(self):
        self.importar([linha_gsan("1"), linha_gsan("2")])
        antes = self.ordem("2").atualizado_em
        self.importar([linha_gsan("1")])
        self.assertEqual(self.ordem("2").atualizado_em, antes)

    def test_ca06_falha_no_banco_desfaz_tudo_e_marca_falhou(self):
        self.importar([linha_gsan("1")])
        with mock.patch(
            "nucleo.upsert.OrdemServico.objects.bulk_update", side_effect=DatabaseError("x")
        ):
            resposta = self.importar([linha_gsan("1", Tipo="MUDOU"), linha_gsan("2")])
        self.assertEqual(resposta.status_code, 500)
        self.assertNotIn("x", resposta.json()["erro"]["mensagem"].split())
        self.assertEqual(OrdemServico.objects.count(), 1)
        self.assertEqual(self.ordem().tipo, "RELIGACAO_AGUA")
        ultima = Importacao.objects.order_by("-id").first()
        self.assertEqual(ultima.status, StatusImportacao.FALHOU)
        self.assertEqual(self.importar([linha_gsan("2")]).status_code, 201)

    def test_ca07_mesmo_numero_em_outro_polo_e_outra_os(self):
        self.importar([linha_gsan("1")])
        cliente_polo_2 = cliente_autenticado(self.analista, self.polo_2.pk)
        self.importar([linha_gsan("1", "UN-21")], cliente_polo_2)
        self.assertEqual(OrdemServico.objects.filter(numero="1").count(), 2)

    def test_ca09_reimportar_o_mesmo_arquivo_nao_duplica(self):
        linhas = [linha_gsan("1"), linha_gsan("2")]
        self.importar(linhas)
        corpo = self.importar(linhas).json()
        self.assertEqual((corpo["resumo"]["novas"], corpo["resumo"]["atualizadas"]), (0, 2))
        self.assertEqual(OrdemServico.objects.count(), 2)

    def test_rn_l05_os_guarda_importacao_de_origem_e_ultima(self):
        primeira = self.importar([linha_gsan("1")]).json()["id"]
        segunda = self.importar([linha_gsan("1")]).json()["id"]
        ordem = self.ordem()
        self.assertEqual(
            (ordem.importacao_origem_id, ordem.importacao_ultima_id), (primeira, segunda)
        )


class ConsultaTest(BaseImportacao):
    def test_detalhe_lista_e_polo_nao_autorizado(self):
        importacao_id = self.importar([linha_gsan("1")]).json()["id"]
        self.assertEqual(self.cliente.get(f"{URL}{importacao_id}/").status_code, 200)
        self.assertEqual(self.cliente.get(f"{URL}999999/").status_code, 404)
        self.assertEqual(self.cliente.get(URL).json()["total"], 1)
        bruno = criar_usuario_com_perfil("b@genios.test", Perfil.ANALISTA_OPERACOES, [self.polo_2])
        cliente_bruno = cliente_autenticado(bruno)
        self.assertEqual(cliente_bruno.get(f"{URL}{importacao_id}/").status_code, 403)
