"""Entrada e saída do Roteirizador (contrato §7)."""

from rest_framework import serializers

from roteirizacao.models import ArquivoDespacho, Operacao, Rota

MAXIMO_OS_POR_ROTA = 99  # capacidade máxima de equipe (HU-009 RN-L03)


class OperacaoSaida(serializers.ModelSerializer):
    class Meta:
        model = Operacao
        fields = ["id", "codigo", "nome"]


class ChavePlanejamentoEntrada(serializers.Serializer):
    operacao_id = serializers.IntegerField(
        error_messages={"required": "Escolha a operação.", "null": "Escolha a operação."}
    )
    data = serializers.DateField(error_messages={"required": "Escolha a data do planejamento."})


class RotaEntrada(ChavePlanejamentoEntrada):
    nome = serializers.CharField(
        max_length=80,
        error_messages={"required": "Informe o nome da rota.", "blank": "Informe o nome da rota."},
    )
    equipe_id = serializers.IntegerField(error_messages={"required": "Escolha a equipe."})
    previsao_inicio = serializers.TimeField(
        error_messages={"required": "Informe a previsão de início."}
    )
    carregamento = serializers.TimeField(
        error_messages={"required": "Informe o horário de carregamento."}
    )
    cor = serializers.RegexField(r"^#[0-9A-Fa-f]{6}$", required=False, allow_blank=True, default="")
    observacao = serializers.CharField(required=False, allow_blank=True, default="", max_length=500)
    ordens_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        min_length=1,
        max_length=MAXIMO_OS_POR_ROTA,
        error_messages={
            "required": "Selecione ao menos uma OS.",
            "min_length": "Selecione ao menos uma OS.",
        },
    )


def _nome(usuario) -> str | None:
    if usuario is None:
        return None
    return usuario.get_full_name() or usuario.email


def ordem_no_mapa(ordem) -> dict:
    """OS como pin do mapa: coordenada da unidade (RN-04)."""
    return {
        "id": ordem.pk,
        "numero": ordem.numero,
        "tipo": ordem.tipo,
        "especificacao": ordem.especificacao,
        "prioridade": ordem.prioridade,
        "unidade": {"codigo": ordem.unidade.codigo, "nome": ordem.unidade.nome},
        "latitude": float(ordem.unidade.latitude),
        "longitude": float(ordem.unidade.longitude),
    }


class RotaSaida(serializers.ModelSerializer):
    equipe = serializers.SerializerMethodField()
    ordens = serializers.SerializerMethodField()
    previsao_inicio = serializers.TimeField(format="%H:%M")
    carregamento = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Rota
        fields = [
            "id",
            "nome",
            "cor",
            "observacao",
            "previsao_inicio",
            "carregamento",
            "equipe",
            "ordens",
        ]

    def get_equipe(self, rota) -> dict:
        equipe = rota.equipe
        return {
            "id": equipe.pk,
            "codigo": equipe.codigo,
            "nome": equipe.nome,
            "placa": equipe.placa,
            "ativa": equipe.ativa,
        }

    def get_ordens(self, rota) -> list[dict]:
        return [ordem_no_mapa(item.ordem_servico) for item in rota.itens.all()]


class ArquivoDespachoSaida(serializers.ModelSerializer):
    gerado_por = serializers.SerializerMethodField()

    class Meta:
        model = ArquivoDespacho
        fields = ["nome_arquivo", "hash_sha256", "total_ordens", "gerado_por", "gerado_em"]

    def get_gerado_por(self, arquivo) -> str | None:
        return _nome(arquivo.gerado_por)


def planejamento_saida(painel) -> dict:
    planejamento = painel.planejamento
    arquivo = getattr(planejamento, "arquivo_despacho", None) if planejamento else None
    return {
        "id": planejamento.pk if planejamento else None,
        "status": planejamento.status if planejamento else "ABERTO",
        "somente_leitura": painel.somente_leitura,
        "motivo_somente_leitura": painel.motivo_somente_leitura,
        "finalizado_em": planejamento.finalizado_em if planejamento else None,
        "finalizado_por": _nome(planejamento.finalizado_por) if planejamento else None,
        "arquivo_rpa": ArquivoDespachoSaida(arquivo).data if arquivo else None,
    }
