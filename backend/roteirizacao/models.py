"""Planejamento do dia, rotas e arquivo de despacho (HU-011, HU-056, HU-013, HU-014).

Um planejamento é identificado por polo + operação + data (HU-013 RN-L01) e toda rota pertence a
um planejamento (HU-011 RN-L03). As OSs continuam no núcleo; aqui só fica o vínculo OS → rota.
"""

from django.conf import settings
from django.db import models

from nucleo.models import Equipe, OrdemServico, Polo


class Operacao(models.Model):
    """Operação do contrato (PSS, XPT Express, Litoral) — catálogo da HU-066 RN-L04."""

    codigo = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=80, unique=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "operação"
        verbose_name_plural = "operações"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class StatusPlanejamento(models.TextChoices):
    ABERTO = "ABERTO", "Em aberto"
    FINALIZADO = "FINALIZADO", "Finalizado"
    DESPACHADO = "DESPACHADO", "Despachado"


class Planejamento(models.Model):
    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="planejamentos")
    operacao = models.ForeignKey(Operacao, on_delete=models.PROTECT, related_name="planejamentos")
    data = models.DateField()
    status = models.CharField(
        max_length=12, choices=StatusPlanejamento.choices, default=StatusPlanejamento.ABERTO
    )
    finalizado_em = models.DateTimeField(null=True, blank=True)
    finalizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="planejamentos_finalizados",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "polo_id", "operacao_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["polo", "operacao", "data"], name="planejamento_unico_por_dia"
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=StatusPlanejamento.values),
                name="planejamento_status_valido",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.polo} · {self.operacao} · {self.data:%d/%m/%Y}"


class Rota(models.Model):
    """Roteiro de uma equipe no dia (HU-056). Campos obrigatórios: RN-L01."""

    planejamento = models.ForeignKey(Planejamento, on_delete=models.PROTECT, related_name="rotas")
    nome = models.CharField(max_length=80)
    equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT, related_name="rotas")
    previsao_inicio = models.TimeField()
    carregamento = models.TimeField()
    cor = models.CharField(max_length=7, blank=True)
    observacao = models.CharField(max_length=500, blank=True)
    criada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="rotas_criadas"
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["planejamento_id", "previsao_inicio", "id"]
        indexes = [models.Index(fields=["equipe", "planejamento"], name="rota_equipe_plan_idx")]

    def __str__(self) -> str:
        return self.nome


class ItemRota(models.Model):
    """OS incluída numa rota, na ordem em que foi selecionada.

    HU-056 RN-L02: a OS pertence a no máximo uma rota. A unicidade fica no banco, não só no código,
    para que duas rotas criadas ao mesmo tempo não levem a mesma OS.
    """

    rota = models.ForeignKey(Rota, on_delete=models.PROTECT, related_name="itens")
    ordem_servico = models.ForeignKey(
        OrdemServico, on_delete=models.PROTECT, related_name="itens_rota"
    )
    sequencia = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "item de rota"
        verbose_name_plural = "itens de rota"
        ordering = ["rota_id", "sequencia"]
        constraints = [
            models.UniqueConstraint(fields=["ordem_servico"], name="os_em_uma_unica_rota"),
            models.UniqueConstraint(fields=["rota", "sequencia"], name="sequencia_unica_na_rota"),
        ]

    def __str__(self) -> str:
        return f"{self.rota} #{self.sequencia}"


class ArquivoDespacho(models.Model):
    """Arquivo RPA gerado de um planejamento finalizado (HU-014, RNF-17).

    O conteúdo fica guardado para que "Baixar novamente" devolva o mesmo arquivo (RN-L02).
    """

    planejamento = models.OneToOneField(
        Planejamento, on_delete=models.PROTECT, related_name="arquivo_despacho"
    )
    nome_arquivo = models.CharField(max_length=120)
    conteudo = models.TextField()
    hash_sha256 = models.CharField(max_length=64)
    total_ordens = models.PositiveIntegerField()
    gerado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="arquivos_despacho"
    )
    gerado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "arquivo de despacho"
        verbose_name_plural = "arquivos de despacho"
        ordering = ["-gerado_em"]

    def __str__(self) -> str:
        return self.nome_arquivo
