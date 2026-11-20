"""Registro das importações da planilha GSAN (HU-001 a HU-004, C4 nível 4 pacote `importacao`)."""

from django.conf import settings
from django.db import models

from nucleo.models import Polo


class StatusImportacao(models.TextChoices):
    RECEBIDA = "RECEBIDA", "Recebida"
    VALIDANDO = "VALIDANDO", "Validando"
    FILTRANDO = "FILTRANDO", "Filtrando"
    GRAVANDO = "GRAVANDO", "Gravando"
    CONCLUIDA = "CONCLUIDA", "Concluída"
    RECUSADA = "RECUSADA", "Recusada"
    FALHOU = "FALHOU", "Falhou"


STATUS_EM_ANDAMENTO = (
    StatusImportacao.RECEBIDA,
    StatusImportacao.VALIDANDO,
    StatusImportacao.FILTRANDO,
    StatusImportacao.GRAVANDO,
)


class Importacao(models.Model):
    """Uma execução de importação. O arquivo em si não é guardado: o disco do Render é efêmero,
    então a rastreabilidade fica no nome original e no hash SHA-256 (HU-001)."""

    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="importacoes")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="importacoes"
    )
    nome_arquivo = models.CharField(max_length=255)
    hash_sha256 = models.CharField(max_length=64)
    status = models.CharField(
        max_length=20, choices=StatusImportacao.choices, default=StatusImportacao.RECEBIDA
    )
    etapa = models.CharField(max_length=30, blank=True)
    percentual = models.PositiveSmallIntegerField(default=0)
    total_linhas = models.PositiveIntegerField(default=0)
    novas = models.PositiveIntegerField(default=0)
    atualizadas = models.PositiveIntegerField(default=0)
    fora_escopo = models.PositiveIntegerField(default=0)
    motivo_falha = models.TextField(blank=True)
    iniciada_em = models.DateTimeField(auto_now_add=True)
    concluida_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "importação"
        verbose_name_plural = "importações"
        ordering = ["-iniciada_em"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=StatusImportacao.values),
                name="importacao_status_valido",
            ),
            models.CheckConstraint(
                condition=models.Q(percentual__lte=100), name="importacao_percentual_ate_100"
            ),
            # 409 do contrato: no máximo uma importação em andamento por polo, garantido no banco.
            models.UniqueConstraint(
                fields=["polo"],
                condition=models.Q(status__in=STATUS_EM_ANDAMENTO),
                name="importacao_unica_em_andamento_por_polo",
            ),
        ]
        indexes = [
            models.Index(fields=["polo", "-iniciada_em"], name="importacao_polo_data_idx"),
            models.Index(fields=["hash_sha256"], name="importacao_hash_idx"),
        ]

    def __str__(self) -> str:
        return f"Importação {self.pk} ({self.status})"


class AlertaImportacao(models.Model):
    """Aviso não bloqueante sobre uma linha da planilha (ex.: prazo preenchido com padrão)."""

    importacao = models.ForeignKey(Importacao, on_delete=models.CASCADE, related_name="alertas")
    linha = models.PositiveIntegerField()
    campo = models.CharField(max_length=60)
    motivo = models.CharField(max_length=255)

    class Meta:
        verbose_name = "alerta de importação"
        verbose_name_plural = "alertas de importação"
        ordering = ["importacao_id", "linha"]

    def __str__(self) -> str:
        return f"Linha {self.linha}: {self.motivo}"
