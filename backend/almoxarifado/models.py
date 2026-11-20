"""Kits e trava de histórico (HU-016, RN-11)."""

from django.conf import settings
from django.db import models

from nucleo.models import Equipe, Polo


class TipoKit(models.Model):
    """Catálogo parametrizável de kits (RF-ALM-02, RNF-27)."""

    codigo = models.CharField(max_length=40, unique=True)
    nome = models.CharField(max_length=120)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "tipo de kit"
        verbose_name_plural = "tipos de kit"
        ordering = ["codigo"]

    def __str__(self) -> str:
        return self.codigo


class ExecucaoKit(models.Model):
    """Quantidade de kits executada por polo e dia: o limite D-1 da trava (RN-11).

    No MVP é populada por seed, porque a importação da planilha de execução (HU-018) está fora do
    escopo (ver nota no contrato da API, seção 6).
    """

    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="execucoes_kit")
    tipo_kit = models.ForeignKey(TipoKit, on_delete=models.PROTECT, related_name="execucoes")
    data = models.DateField()
    quantidade = models.PositiveIntegerField()

    class Meta:
        verbose_name = "execução de kit"
        verbose_name_plural = "execuções de kit"
        ordering = ["-data", "polo_id", "tipo_kit_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["polo", "tipo_kit", "data"], name="execucao_kit_unica_por_dia"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.tipo_kit} {self.data}: {self.quantidade}"


class SaidaKit(models.Model):
    """Saída de kits para uma equipe. A soma do dia não pode passar da execução D-1 (RN-11)."""

    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="saidas_kit")
    equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT, related_name="saidas_kit")
    tipo_kit = models.ForeignKey(TipoKit, on_delete=models.PROTECT, related_name="saidas")
    quantidade = models.PositiveIntegerField()
    # Data separada do instante para somar "saídas de hoje" com índice simples.
    data = models.DateField()
    registrado_em = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="saidas_kit"
    )

    class Meta:
        verbose_name = "saída de kit"
        verbose_name_plural = "saídas de kit"
        ordering = ["-registrado_em"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade__gt=0), name="saida_kit_quantidade_positiva"
            ),
        ]
        indexes = [
            models.Index(fields=["polo", "tipo_kit", "data"], name="saida_kit_polo_kit_data_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.tipo_kit} x{self.quantidade} -> {self.equipe}"
