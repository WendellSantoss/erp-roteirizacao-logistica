---
id: HU-043
titulo: Ver o impacto financeiro da glosa potencial
ordem: 59
modulo: Gerencial
epico: EP-D Fechamento, auditoria e faturamento
tela: "Gerencial" › cartão "Impacto financeiro"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-GER-03]
regras: [RN-18]
nao_funcionais: [RNF-21]
depende_de: [HU-042]
---

# HU-043 — Ver o impacto financeiro da glosa potencial

## História
Como **Gerente de Contrato**, quero **ver quanto dinheiro está em risco por OSs executadas e não
validadas**, para **decidir onde concentrar a contestação junto à fiscalização**.

## Regras de negócio
- **RN-18** — Glosa potencial = valor da produção bruta − valor da produção validada, no período e polo.

## Critérios de aceite
CA01 — Cartão
Dado bruta R$ 312.480,00 e validada R$ 204.624,00
Quando abro o Gerencial
Então o cartão mostra "−R$ 107.856,00" e o rótulo "glosa potencial em aberto" (com forma curta
"−R$ 107k" quando o espaço for pequeno).

CA02 — Detalhar
Dado o cartão
Quando clico nele
Então vou para a lista de invalidações (HU-061) e OSs executadas ainda não validadas, filtradas
pelo mesmo período e polo.

CA03 — Zero
Dado bruta igual à validada
Quando abro
Então o cartão mostra "R$ 0,00" sem destaque de alerta.
