---
id: HU-064
titulo: Fechar e reabrir o ciclo de medição
ordem: 64
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: — (a desenhar)
fase: 3
prioridade: MVP
status: proposta
requisitos: [RF-AUD-08 (proposto)]
regras: [RN-15, RN-19]
nao_funcionais: [RNF-12, RNF-17]
depende_de: [HU-044, HU-F11]
---

# HU-064 — Fechar e reabrir o ciclo de medição

> **Proposta — validar com o grupo.** RN-15 cita fechamento e reabertura, e o estado "Faturada"
> não tem transição definida na ERS.

## História
Como **Gerente de Contrato**, quero **fechar o ciclo de medição de um polo, congelando o BM**,
para **faturar com segurança de que nada vai mudar depois**; e **reabrir com justificativa
quando for preciso corrigir**.

## Regras de negócio
- **RN-19** — O BM considera só OSs "Validada" do ciclo.
- **RN-L01** — Ciclo = polo + período (início e fim). Período padrão: mês civil (proposta).
- **RN-L02** — Fechar: as OSs "Validada" do ciclo passam a "Faturada", o BM é congelado (valores
  e lista de OSs gravados), e a grade fica somente leitura (RN-15).
- **RN-L03** — Reabrir: só o Gerente, com justificativa ≥ 20 caracteres; as OSs "Faturada" do
  ciclo voltam a "Validada"; o BM congelado anterior fica guardado como versão.
- **RN-L04** — Fechar e reabrir são ações críticas (RNF-12).

## Critérios de aceite
CA01 — Fechar
Dado o ciclo Polo 1 · julho/2026 com 812 OSs validadas somando R$ 204.624,00
Quando o Gerente fecha o ciclo
Então as 812 passam a "Faturada", o BM fica congelado com esse total, e a grade de julho fica
somente leitura.

CA02 — Rastreável (RNF-17)
Dado o ciclo fechado
Quando consulto o BM
Então vejo exatamente as 812 OSs e os valores por item, mesmo que a tabela de preços mude depois.

CA03 — Reabrir
Dado o ciclo fechado
Quando o Gerente reabre com "Correção de 3 OSs com valor errado"
Então as 812 voltam a "Validada", a grade volta a ser editável e o BM anterior fica como "versão 1".

CA04 — Sem permissão
Dado o Auditor
Quando chama fechar ou reabrir na API
Então recebe `403`.

## Dúvidas em aberto
- O ciclo de medição do contrato é mensal? Começa no dia 1?
