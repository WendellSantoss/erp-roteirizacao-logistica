---
id: HU-040
titulo: Registrar cada correção feita na grade
ordem: 55
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › histórico da linha (a desenhar)
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-AUD-05]
regras: []
nao_funcionais: [RNF-15, RNF-16]
depende_de: [HU-045]
---

# HU-040 — Registrar cada correção feita na grade

## História
Como **Gerente de Contrato**, quero **saber quem mudou o quê em cada OS auditada, e quando**,
para **responder à concessionária e a auditorias internas sobre qualquer valor faturado**.

## Critérios de aceite
CA01 — Registro
Dado o Auditor "Carla" mudando o Valor da OS 4471203 de R$ 250,00 para R$ 200,00 às 10:15
Quando a alteração é salva
Então existe o registro: OS, campo "Valor", anterior "250,00", novo "200,00", autor "Carla",
data/hora 11/07/2026 10:15, justificativa.

CA02 — Consulta pela linha
Dado a OS com 3 alterações
Quando abro o histórico da linha
Então vejo as 3, da mais recente para a mais antiga.

CA03 — Imutável (RNF-16)
Dado um registro de alteração
Quando qualquer usuário (inclusive Administrador) tenta editar ou apagar pela API
Então a operação não existe ou é recusada.

CA04 — Mesma transação
Dado uma falha ao gravar o registro de alteração
Quando a edição é salva
Então a edição também não é aplicada (alteração sem registro não existe).
