---
id: HU-053
titulo: Confirmar antes que o assistente execute uma ação
ordem: 80
modulo: Assistente
epico: EP-E Inteligência e suporte à decisão
tela: "Assistente GeniOS" › diálogo de confirmação
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ASS-05]
regras: [RN-21]
nao_funcionais: [RNF-15]
depende_de: [HU-049]
---

# HU-053 — Confirmar antes que o assistente execute uma ação

## História
Como **usuário do GeniOS**, quero **ver exatamente o que o assistente vai fazer e confirmar antes**,
para **nunca ter uma alteração feita por engano de interpretação**.

## Regras de negócio
- **RN-L01** — A confirmação mostra a ação, os registros afetados e os valores (ex.: "Atribuir 12
  OSs à Equipe B em 12/07").
- **RN-L02** — A confirmação vale uma vez e expira em 5 min.
- **RN-L03** — O servidor só executa a ação com uma confirmação válida do próprio usuário; o
  assistente sozinho não consegue executar.

## Critérios de aceite
CA01 — Confirmar
Dado a sugestão "Atribuir 12 OSs à Equipe B em 12/07"
Quando clico em "Atribuir" no diálogo
Então a ação é executada, aparece o toast de sucesso e a trilha registra "via assistente".

CA02 — Cancelar
Dado o diálogo
Quando clico em "Cancelar"
Então nada é alterado e o assistente registra "ação cancelada".

CA03 — Sem confirmação
Dado uma ação proposta
Quando o assistente tenta executá-la sem confirmação do usuário
Então o servidor recusa.

CA04 — Expirada
Dado uma confirmação de 6 min atrás
Quando clico em "Atribuir"
Então aparece "Confirmação expirada — peça de novo ao assistente".
