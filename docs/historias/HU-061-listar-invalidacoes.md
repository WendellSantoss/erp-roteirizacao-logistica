---
id: HU-061
titulo: Ver as OSs reprovadas pela fiscalização
ordem: 62
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › "Invalidações" ("OSs reprovadas pela fiscalização CAGEPA")
fase: 3
prioridade: MVP
status: proposta
requisitos: [RF-AUD-06 (proposto)]
regras: [RN-14]
nao_funcionais: [RNF-20]
depende_de: [HU-018]
---

# HU-061 — Ver as OSs reprovadas pela fiscalização

> **Proposta — validar com o grupo.** O estado "Invalidada" e a entidade Invalidação existem na
> ERS, e a aba aparece no protótipo, mas não há requisito.

## História
Como **Auditor / Faturista**, quero **uma lista das OSs reprovadas pela fiscalização da
concessionária, com motivo e inspetor**, para **tratar cada glosa antes do fechamento do ciclo**.

## Critérios de aceite
CA01 — Lista
Dado 12 OSs invalidadas no Polo 1
Quando abro "Invalidações"
Então vejo o contador "12" e, para cada OS: número, motivo, inspetor, data e status de tratamento.

CA02 — Valor em risco
Dado as 12
Quando olho o topo da lista
Então vejo o valor somado delas (glosa potencial, RN-18).

CA03 — Sai ao validar
Dado uma OS da lista
Quando ela tem a validação forçada (HU-062)
Então sai da lista e o contador diminui.

CA04 — Vazio
Dado nenhuma invalidação
Quando abro
Então vejo "Nenhuma invalidação pendente".
