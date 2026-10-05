---
id: HU-037
titulo: Enviar a planilha de execução do GSAN
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › "Subir planilha de fechamento"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-AUD-01]
regras: []
nao_funcionais: [RNF-05, RNF-07, RNF-19]
depende_de: [HU-001, HU-002, HU-F08]
---

# HU-037 — Enviar a planilha de execução do GSAN

## História
Como **Auditor / Faturista**, quero **enviar a planilha de execução do GSAN informando a data de
referência**, para **confrontar o que foi despachado com o que foi executado e fiscalizado**.

## Regras de negócio
- **RN-L01** — Mesmas regras de arquivo da HU-001 (`.xlsx`, até 25 MB, um por vez) e de layout
  da HU-002, com as colunas da planilha de execução.
- **RN-L02** — Data de referência obrigatória, não futura.
- **RN-L03** — Uma planilha por polo e data de referência. Enviar outra para a mesma data exige
  confirmação "substituir" e só é permitido com o ciclo aberto (RN-15).
- **RN-L04** — Processamento assíncrono e tudo ou nada.

## Critérios de aceite
CA01 — Enviar
Dado o Auditor no Polo 1
Quando envia `execucao_2026-07-11.xlsx` com data de referência 11/07/2026
Então a planilha é registrada e a conciliação (HU-018) começa; o cabeçalho mostra "Planilha de
execução GSAN · 11/07/2026".

CA02 — Sem data
Dado nenhuma data de referência
Quando envio
Então aparece "Informe a data de referência".

CA03 — Substituir
Dado uma planilha de 11/07 já enviada, ciclo aberto
Quando envio outra para 11/07
Então aparece a confirmação "Já existe planilha de 11/07. Substituir?"; ao confirmar, a
conciliação é refeita e a anterior fica guardada no histórico.

CA04 — Ciclo fechado
Dado o ciclo que contém 11/07 fechado
Quando envio planilha de 11/07
Então é recusado com "Ciclo fechado — reabra o ciclo para alterar".
