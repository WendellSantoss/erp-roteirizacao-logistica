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
    ("caio.coordenador@genios.test", "Caio", "Coordenador", Perfil.COORDENADOR, True, ["*"]),
]

# Por polo: (sufixo do código, bairro, no_escopo, latitude, longitude). Bairros de João Pessoa
# com coordenada aproximada do centro do bairro (dentro da área da HU-005 RN-L02). A unidade "08"
# fica sem coordenada para exercitar a HU-024 e a "09" fica fora do escopo (HU-003).
UNIDADES = {
    "POLO_1": [
        ("01", "Centro", True, "-7.119500", "-34.882000"),
        ("02", "Tambiá", True, "-7.113500", "-34.877000"),
        ("03", "Jaguaribe", True, "-7.130000", "-34.874000"),
        ("04", "Torre", True, "-7.124000", "-34.860000"),
        ("05", "Cruz das Armas", True, "-7.142000", "-34.889000"),
        ("06", "Varadouro", True, "-7.110500", "-34.888500"),
        ("08", "Roger", True, None, None),
        ("09", "Unidade Conveniada Central", False, None, None),
    ],
    "POLO_2": [
        ("01", "Bessa", True, "-7.083200", "-34.833600"),
        ("02", "Manaíra", True, "-7.096000", "-34.835000"),
        ("03", "Tambaú", True, "-7.114000", "-34.825000"),
        ("04", "Cabo Branco", True, "-7.125000", "-34.824000"),
        ("05", "Aeroclube", True, "-7.092000", "-34.840000"),
        ("06", "Jardim Oceania", True, "-7.101000", "-34.832000"),
        ("08", "João Agripino", True, None, None),
        ("09", "Unidade Conveniada Norte", False, None, None),
    ],
    "POLO_3": [
        ("01", "Mangabeira", True, "-7.170000", "-34.836000"),
        ("02", "Valentina", True, "-7.201000", "-34.843000"),
        ("03", "Bancários", True, "-7.151000", "-34.842000"),
        ("04", "José Américo", True, "-7.160000", "-34.856000"),
        ("05", "Geisel", True, "-7.162000", "-34.877000"),
        ("06", "Cristo Redentor", True, "-7.149000", "-34.870000"),
        ("08", "Paratibe", True, None, None),
        ("09", "Unidade Conveniada Sul", False, None, None),
    ],
}

# Por polo: (sufixo, nome da dupla, ativa, prefixo da placa, capacidade diária). A placa recebe o
# número do polo no fim para ser única no sistema (HU-009 RN-L02).
EQUIPES = [
    ("01", "João / Marcos", True, "QRT2A1", 25),
    ("02", "Rita / Paulo", True, "QRT3B2", 20),
    ("03", "Equipe Reserva", False, "QRT4C3", 25),
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

# Estados distribuídos para que pendências, mapa e contadores tenham variedade. Não há OS
# "Roteirizada" no seed: esse estado só existe com rota, criada pelo Roteirizador (HU-056).
ESTADOS_OS = [
    EstadoOS.PENDENTE,
    EstadoOS.APTA_A_ROTEIRIZAR,
    EstadoOS.PENDENTE,
    EstadoOS.APTA_A_ROTEIRIZAR,
    EstadoOS.APTA_A_ROTEIRIZAR,
    EstadoOS.PENDENTE,
    EstadoOS.APTA_A_ROTEIRIZAR,
    EstadoOS.DESCONSIDERADA,
]
OS_POR_POLO = 30
