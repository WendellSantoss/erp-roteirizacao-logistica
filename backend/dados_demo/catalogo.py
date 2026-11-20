"""Dados fictícios de demonstração. Nenhum dado aqui corresponde a pessoa ou imóvel real.

Usuários usam o domínio reservado ``.test`` (RFC 2606); a senha vem da variável de ambiente
``SENHA_USUARIOS_DEMO`` para não ficar versionada.
"""

from nucleo.models import EstadoOS, Perfil

POLOS = [
    ("POLO_1", "Polo 1 - Central"),
    ("POLO_2", "Polo 2 - Norte"),
    ("POLO_3", "Polo 3 - Sul"),
]

# (email, nome, sobrenome, perfil, pode_visualizar_todos, polos autorizados)
USUARIOS = [
    ("ana.analista@genios.test", "Ana", "Analista", Perfil.ANALISTA_OPERACOES, True, ["*"]),
    ("bruno.norte@genios.test", "Bruno", "Norte", Perfil.ANALISTA_OPERACOES, False, ["POLO_2"]),
    ("carlos.almox@genios.test", "Carlos", "Almoxarife", Perfil.ALMOXARIFE, False, ["POLO_1"]),
    ("gabriela.gerente@genios.test", "Gabriela", "Gerente", Perfil.GERENTE_CONTRATO, True, ["*"]),
    ("alice.auditora@genios.test", "Alice", "Auditora", Perfil.AUDITOR, True, ["*"]),
    ("davi.admin@genios.test", "Davi", "Admin", Perfil.ADMINISTRADOR, True, ["*"]),
]

# Por polo: (sufixo do código, nome, no_escopo, latitude, longitude). A última fica fora do escopo
# para exercitar o filtro da HU-003.
UNIDADES = [
    ("01", "ETA", True, "-3.731900", "-38.526700"),
    ("02", "Escritório Regional", True, "-3.745000", "-38.523000"),
    ("03", "Reservatório", True, "-3.760000", "-38.540000"),
    ("09", "Unidade Conveniada", False, None, None),
]

# Por polo: (sufixo, nome da dupla, ativa)
EQUIPES = [
    ("01", "João / Marcos", True),
    ("02", "Rita / Paulo", True),
    ("03", "Equipe Reserva", False),
]

TIPOS_KIT = [
    ("KIT_LIGACAO_NOVA_1_2", "Kit Ligação Nova 1/2"),
    ("KIT_HIDROMETRO", "Kit Hidrômetro"),
    ("KIT_SUPRESSAO", "Kit Supressão"),
    ("KIT_RELIGACAO", "Kit Religação"),
]

# Execução diária por polo e kit (base para a trava D-1). Ausência = executado 0 (HU-016 CA04/CA05).
EXECUCAO_DIARIA = {
    "POLO_1": {"KIT_LIGACAO_NOVA_1_2": 25, "KIT_HIDROMETRO": 10, "KIT_RELIGACAO": 8},
    "POLO_2": {"KIT_LIGACAO_NOVA_1_2": 12, "KIT_RELIGACAO": 5},
    "POLO_3": {"KIT_LIGACAO_NOVA_1_2": 18, "KIT_HIDROMETRO": 6, "KIT_SUPRESSAO": 3},
}
DIAS_DE_EXECUCAO = 14

TIPOS_SERVICO = [
    ("RELIGACAO_AGUA", "Religação no cavalete", 24),
    ("LIGACAO_NOVA", "Ligação nova de água 1/2", 72),
    ("TROCA_HIDROMETRO", "Substituição de hidrômetro", 48),
    ("SUPRESSAO", "Supressão de ligação por débito", 48),
]

# Estados distribuídos para que a listagem e os contadores tenham variedade.
ESTADOS_OS = [
    EstadoOS.PENDENTE,
    EstadoOS.PENDENTE,
    EstadoOS.PENDENTE,
    EstadoOS.APTA_A_ROTEIRIZAR,
    EstadoOS.PENDENTE,
    EstadoOS.ROTEIRIZADA,
    EstadoOS.PENDENTE,
    EstadoOS.DESCONSIDERADA,
]
OS_POR_POLO = 16
