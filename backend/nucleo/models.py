"""Entidades compartilhadas por todos os módulos (C4 nível 4, pacote `nucleo`).

O núcleo não depende de nenhum módulo de negócio (regra 5 do C4). A única exceção é de
esquema, não de código: a OS guarda a importação que a criou e a última que a atualizou
(HU-004 RN-L05) por referência textual ``"importacao.Importacao"``, sem import Python.
"""

from django.conf import settings
from django.db import models


class Polo(models.Model):
    """Base operacional regional. Cadastro: polo novo não exige código (RNF-26)."""

    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=80, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.nome


class Perfil(models.TextChoices):
    """Perfis da ERS §2.2 usados na matriz de acesso da HU-020."""

    GERENTE_CONTRATO = "GERENTE_CONTRATO", "Gerente de Contrato"
    COORDENADOR = "COORDENADOR", "Coordenador"
    ANALISTA_OPERACOES = "ANALISTA_OPERACOES", "Analista de Operações"
    ALMOXARIFE = "ALMOXARIFE", "Almoxarife"
    AUDITOR = "AUDITOR", "Auditor"
    ADMINISTRADOR = "ADMINISTRADOR", "Administrador"


class PerfilUsuario(models.Model):
    """Perfil e polos autorizados de um usuário (HU-019, HU-020).

    Estende o ``auth.User`` do Django em vez de substituí-lo: o esqueleto da Etapa 2 já aplicou
    as migrations de ``auth`` no Neon, e trocar o ``AUTH_USER_MODEL`` exigiria recriar o banco.
    """

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_acesso"
    )
    perfil = models.CharField(max_length=30, choices=Perfil.choices)
    pode_visualizar_todos = models.BooleanField(default=False)
    polos_autorizados = models.ManyToManyField(Polo, related_name="perfis_usuario")

    class Meta:
        verbose_name = "perfil de usuário"
        verbose_name_plural = "perfis de usuário"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(perfil__in=Perfil.values), name="perfil_usuario_perfil_valido"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.usuario} ({self.perfil})"


class Unidade(models.Model):
    """Unidade operacional do GSAN. ``no_escopo`` alimenta o filtro de escopo (HU-003)."""

    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="unidades")
    codigo = models.CharField(max_length=20)
    nome = models.CharField(max_length=120)
    no_escopo = models.BooleanField(default=True)
    # Sem PostGIS no MVP (Render gratuito); lat/long simples bastam para exibir pins.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["polo_id", "codigo"]
        constraints = [
            models.UniqueConstraint(fields=["polo", "codigo"], name="unidade_unica_por_polo"),
        ]

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"


class Equipe(models.Model):
    """Equipe de campo vinculada a um único polo (RF-EQP-03)."""

    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="equipes")
    codigo = models.CharField(max_length=20)
    nome = models.CharField(max_length=120)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["polo_id", "codigo"]
        constraints = [
            models.UniqueConstraint(fields=["polo", "codigo"], name="equipe_unica_por_polo"),
        ]
        indexes = [models.Index(fields=["polo", "ativa"], name="equipe_polo_ativa_idx")]

    def __str__(self) -> str:
        return f"{self.codigo} ({self.nome})"


class EstadoOS(models.TextChoices):
    """Estados do ciclo de vida da OS (HU-F11). Transições ficam em ``CicloDeVidaOS``."""

    PENDENTE = "PENDENTE", "Pendente"
    APTA_A_ROTEIRIZAR = "APTA_A_ROTEIRIZAR", "Apta a roteirizar"
    DESCONSIDERADA = "DESCONSIDERADA", "Desconsiderada"
    ROTEIRIZADA = "ROTEIRIZADA", "Roteirizada"
    DESPACHADA = "DESPACHADA", "Despachada"
    EXECUTADA = "EXECUTADA", "Executada"
    INVALIDADA = "INVALIDADA", "Invalidada"
    VALIDADA = "VALIDADA", "Validada"
    FATURADA = "FATURADA", "Faturada"


class OrdemServico(models.Model):
    """Ordem de Serviço. Chave natural ``(numero, polo)`` (RN-01).

    Os campos se dividem em dois grupos (RN-02): os que vêm do GSAN e podem ser atualizados a
    cada importação (``CAMPOS_GSAN``) e o tratamento feito no GeniOS, que nunca é sobrescrito.
    """

    CAMPOS_GSAN = (
        "unidade",
        "tipo",
        "especificacao",
        "numero_imovel",
        "cidade",
        "setor",
        "quadra",
        "abertura",
        "prazo_horas",
    )

    numero = models.CharField(max_length=30)
    polo = models.ForeignKey(Polo, on_delete=models.PROTECT, related_name="ordens_servico")

    # Dados do GSAN (atualizáveis pela importação)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="ordens_servico")
    tipo = models.CharField(max_length=60)
    especificacao = models.CharField(max_length=255)
    numero_imovel = models.CharField(max_length=30, blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    setor = models.CharField(max_length=10, blank=True)
    quadra = models.CharField(max_length=10, blank=True)
    abertura = models.DateTimeField()
    prazo_horas = models.PositiveIntegerField()

    # Tratamento GeniOS (nunca sobrescrito pela importação)
    estado = models.CharField(max_length=20, choices=EstadoOS.choices, default=EstadoOS.PENDENTE)
    prioridade = models.BooleanField(default=False)
    equipe = models.ForeignKey(
        Equipe, on_delete=models.PROTECT, null=True, blank=True, related_name="ordens_servico"
    )

    # Rastreabilidade da carga (HU-004 RN-L05)
    importacao_origem = models.ForeignKey(
        "importacao.Importacao",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordens_criadas",
    )
    importacao_ultima = models.ForeignKey(
        "importacao.Importacao",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordens_atualizadas",
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ordem de serviço"
        verbose_name_plural = "ordens de serviço"
        ordering = ["abertura"]
        constraints = [
            models.UniqueConstraint(fields=["numero", "polo"], name="os_numero_polo_unica"),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadoOS.values), name="os_estado_valido"
            ),
            models.CheckConstraint(
                condition=models.Q(prazo_horas__gt=0), name="os_prazo_horas_positivo"
            ),
        ]
        indexes = [
            # GET /ordens-servico/ filtra por polo + estado e ordena por abertura.
            models.Index(fields=["polo", "estado", "abertura"], name="os_polo_estado_abertura_idx"),
            models.Index(
                fields=["polo", "estado"],
                name="os_prioritarias_idx",
                condition=models.Q(prioridade=True),
            ),
        ]

    def __str__(self) -> str:
        return f"OS {self.numero} ({self.polo_id})"

    @property
    def desconsiderada(self) -> bool:
        """Derivado do estado para não haver duas fontes de verdade (contrato expõe o campo)."""
        return self.estado == EstadoOS.DESCONSIDERADA


class OrigemAuditoria(models.TextChoices):
    TELA = "TELA", "Tela"
    IMPORTACAO = "IMPORTACAO", "Importação"
    API = "API", "API"
    SISTEMA = "SISTEMA", "Sistema"


class RegistroAuditoria(models.Model):
    """Trilha imutável (RNF-16, HU-045). UPDATE e DELETE são bloqueados por trigger no banco."""

    polo = models.ForeignKey(
        Polo, on_delete=models.PROTECT, null=True, blank=True, related_name="registros_auditoria"
    )
    entidade = models.CharField(max_length=60)
    entidade_id = models.BigIntegerField(null=True, blank=True)
    campo = models.CharField(max_length=60)
    valor_anterior = models.JSONField(null=True, blank=True)
    valor_novo = models.JSONField(null=True, blank=True)
    justificativa = models.TextField(blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="registros_auditoria",
    )
    origem = models.CharField(max_length=20, choices=OrigemAuditoria.choices)
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "registro de auditoria"
        verbose_name_plural = "registros de auditoria"
        ordering = ["-registrado_em"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(origem__in=OrigemAuditoria.values),
                name="auditoria_origem_valida",
            ),
        ]
        indexes = [
            models.Index(fields=["entidade", "entidade_id"], name="auditoria_entidade_idx"),
            models.Index(fields=["polo", "-registrado_em"], name="auditoria_polo_data_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.entidade}#{self.entidade_id}.{self.campo}"
