"""Entrada e saída do almoxarifado (contrato §6)."""

from rest_framework import serializers

from almoxarifado.models import SaidaKit


class SaidaKitEntrada(serializers.Serializer):
    equipe_id = serializers.IntegerField(error_messages={"required": "Informe a equipe."})
    kit_id = serializers.IntegerField(error_messages={"required": "Informe o tipo de kit."})
    quantidade = serializers.IntegerField(
        min_value=1,
        error_messages={
            "required": "Informe a quantidade.",
            "min_value": "A quantidade deve ser maior que zero.",
        },
    )


class FiltroDataEntrada(serializers.Serializer):
    data = serializers.DateField(required=False, allow_null=True, default=None)


def _nome(usuario) -> str:
    return usuario.get_full_name() or usuario.email


class SaidaKitRegistrada(serializers.ModelSerializer):
    tipo_kit = serializers.CharField(source="tipo_kit.codigo")
    data_saida = serializers.DateTimeField(source="registrado_em")
    registrado_por = serializers.SerializerMethodField()

    class Meta:
        model = SaidaKit
        fields = [
            "id",
            "polo_id",
            "equipe_id",
            "tipo_kit",
            "quantidade",
            "data_saida",
            "registrado_por",
        ]

    def get_registrado_por(self, saida) -> str:
        return _nome(saida.registrado_por)


class SaidaKitListada(serializers.ModelSerializer):
    polo = serializers.CharField(source="polo.nome")
    equipe = serializers.SerializerMethodField()
    tipo_kit = serializers.CharField(source="tipo_kit.codigo")
    data_saida = serializers.DateTimeField(source="registrado_em")
    registrado_por = serializers.SerializerMethodField()

    class Meta:
        model = SaidaKit
        fields = ["id", "polo", "equipe", "tipo_kit", "quantidade", "data_saida", "registrado_por"]

    def get_equipe(self, saida) -> str:
        return f"{saida.equipe.codigo} ({saida.equipe.nome})"

    def get_registrado_por(self, saida) -> str:
        return _nome(saida.registrado_por)
