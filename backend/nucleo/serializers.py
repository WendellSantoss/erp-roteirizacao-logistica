"""Validação de entrada e formatação de saída do núcleo (contrato §3 e §5)."""

from dataclasses import asdict

from rest_framework import serializers

from nucleo.models import Equipe, EstadoOS, OrdemServico, Polo, RegistroAuditoria

TAMANHO_PADRAO_PAGINA = 50
TAMANHO_MAXIMO_PAGINA = 200


def validar(classe_serializer, dados) -> dict:
    """Valida a entrada com o serializer; erro vira 400 no formato do contrato."""
    entrada = classe_serializer(data=dados)
    entrada.is_valid(raise_exception=True)
    return entrada.validated_data


# ── Autenticação (HU-019/020) ─────────────────────────────────────────────────


class LoginEntrada(serializers.Serializer):
    email = serializers.EmailField(error_messages={"required": "Informe o e-mail."})
    senha = serializers.CharField(
        trim_whitespace=False, error_messages={"required": "Informe a senha."}
    )


class PoloSaida(serializers.ModelSerializer):
    class Meta:
        model = Polo
        fields = ["id", "codigo", "nome"]


class UsuarioSaida(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    email = serializers.EmailField()
    perfil = serializers.CharField()
    pode_visualizar_todos = serializers.BooleanField()
    polos_autorizados = PoloSaida(many=True)
    modulos = serializers.ListField(child=serializers.CharField())


class LoginSaida(serializers.Serializer):
    access_token = serializers.CharField()
    usuario = UsuarioSaida()


# ── Ordens de serviço (HU-006/007/008) ────────────────────────────────────────


class FiltroOrdensEntrada(serializers.Serializer):
    estado = serializers.ChoiceField(choices=EstadoOS.choices, default=EstadoOS.PENDENTE)
    prioridade = serializers.BooleanField(required=False, allow_null=True, default=None)
    atrasada = serializers.BooleanField(required=False, allow_null=True, default=None)
    busca = serializers.CharField(required=False, default="", max_length=60)
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(
        required=False,
        default=TAMANHO_PADRAO_PAGINA,
        min_value=1,
        max_value=TAMANHO_MAXIMO_PAGINA,
    )


class OrdemServicoSaida(serializers.ModelSerializer):
    polo = serializers.SerializerMethodField()
    unidade = serializers.SerializerMethodField()
    desconsiderada = serializers.BooleanField(read_only=True)

    class Meta:
        model = OrdemServico
        fields = [
            "id",
            "numero",
            "polo",
            "unidade",
            "tipo",
            "especificacao",
            "numero_imovel",
            "cidade",
            "setor",
            "quadra",
            "estado",
            "prioridade",
            "desconsiderada",
            "equipe_id",
            "abertura",
            "prazo_horas",
        ]

    def get_polo(self, ordem) -> dict:
        return {"id": ordem.polo_id, "nome": ordem.polo.nome}

    def get_unidade(self, ordem) -> dict:
        unidade = ordem.unidade
        return {
            "codigo": unidade.codigo,
            "nome": unidade.nome,
            "latitude": unidade.latitude,
            "longitude": unidade.longitude,
        }


def ordem_com_prazos(ordem, prazos) -> dict:
    """Junta os dados da OS com decorrido/atraso calculados no service."""
    return {**OrdemServicoSaida(ordem).data, **asdict(prazos)}


class PrioridadeEntrada(serializers.Serializer):
    prioridade = serializers.BooleanField(
        error_messages={"required": "Informe o campo prioridade."}
    )
    justificativa = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=500
    )


class DesconsiderarEntrada(serializers.Serializer):
    justificativa = serializers.CharField(
        max_length=500,
        error_messages={
            "required": "Informe a justificativa para desconsiderar a OS.",
            "blank": "Informe a justificativa para desconsiderar a OS.",
        },
    )


# ── Auditoria e equipes ───────────────────────────────────────────────────────


class FiltroAuditoriaEntrada(serializers.Serializer):
    entidade = serializers.CharField(required=False, default="", max_length=60)
    entidade_id = serializers.IntegerField(required=False, allow_null=True, default=None)


class RegistroAuditoriaSaida(serializers.ModelSerializer):
    autor = serializers.SerializerMethodField()

    class Meta:
        model = RegistroAuditoria
        fields = [
            "id",
            "entidade",
            "entidade_id",
            "campo",
            "valor_anterior",
            "valor_novo",
            "justificativa",
            "autor",
            "origem",
            "registrado_em",
        ]

    def get_autor(self, registro) -> str:
        if registro.autor is None:
            return "Sistema"
        return registro.autor.get_full_name() or registro.autor.email


class FiltroEquipesEntrada(serializers.Serializer):
    ativa = serializers.BooleanField(required=False, allow_null=True, default=None)


class EquipeSaida(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ["id", "codigo", "nome", "polo_id", "ativa"]
