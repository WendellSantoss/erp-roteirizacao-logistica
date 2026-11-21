"""Formatação das respostas de importação (contrato §4)."""

from rest_framework import serializers

from importacao.models import AlertaImportacao, Importacao, StatusImportacao
from nucleo.serializers import TAMANHO_MAXIMO_PAGINA


def nome_do_usuario(usuario) -> str:
    return usuario.get_full_name() or usuario.email


class AlertaSaida(serializers.ModelSerializer):
    class Meta:
        model = AlertaImportacao
        fields = ["linha", "campo", "motivo"]


class ImportacaoSaida(serializers.ModelSerializer):
    resumo = serializers.SerializerMethodField()
    alertas = AlertaSaida(many=True, read_only=True)
    motivo_falha = serializers.SerializerMethodField()

    class Meta:
        model = Importacao
        fields = [
            "id",
            "polo_id",
            "nome_arquivo",
            "status",
            "etapa",
            "percentual",
            "hash_sha256",
            "resumo",
            "alertas",
            "motivo_falha",
            "iniciada_em",
            "concluida_em",
        ]

    def get_resumo(self, importacao) -> dict:
        return {
            "total_linhas": importacao.total_linhas,
            "novas": importacao.novas,
            "atualizadas": importacao.atualizadas,
            "fora_escopo": importacao.fora_escopo,
        }

    def get_motivo_falha(self, importacao) -> str | None:
        return importacao.motivo_falha or None


class ImportacaoResumoSaida(serializers.ModelSerializer):
    polo = serializers.CharField(source="polo.nome")
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = Importacao
        fields = [
            "id",
            "polo",
            "usuario",
            "nome_arquivo",
            "status",
            "hash_sha256",
            "total_linhas",
            "novas",
            "atualizadas",
            "fora_escopo",
            "iniciada_em",
        ]

    def get_usuario(self, importacao) -> str:
        return nome_do_usuario(importacao.usuario)


class FiltroImportacoesEntrada(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=StatusImportacao.choices, required=False, allow_blank=True, default=""
    )
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(
        required=False, default=20, min_value=1, max_value=TAMANHO_MAXIMO_PAGINA
    )
