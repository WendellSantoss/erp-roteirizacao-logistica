---
id: HU-038
titulo: Ver a grade de auditoria da execução
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › "Grade de auditoria"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-AUD-03]
regras: [RN-16]
nao_funcionais: [RNF-02, RNF-21]
depende_de: [HU-018]
---

# HU-038 — Ver a grade de auditoria da execução

## História
Como **Auditor / Faturista**, quero **uma grade com OS, serviço, equipe, foto, status e valor de
cada OS da data de referência**, para **revisar a execução antes do faturamento**.

## Critérios de aceite
CA01 — Grade
Dado a data de referência 11/07 conciliada no Polo 1
Quando abro a grade
Então vejo uma linha por OS com: OS, Serviço, Equipe, Foto (tem/não tem, com link para abrir),
Status (Executada, Invalidada, Validada) e Valor em R$.

CA02 — Filtros
Dado a grade
Quando filtro por status "Invalidada" ou por equipe
Então só as linhas correspondentes aparecem, com o total de linhas e o valor somado.

CA03 — Desempenho
Dado 5.000 linhas na data
Quando abro a grade
Então a primeira página aparece em até 2 s.

CA04 — Ciclo fechado
Dado o ciclo fechado
Quando abro a grade
Então ela está somente leitura, com o aviso "Ciclo fechado em <data> por <usuário>".

## Dúvidas em aberto
- De onde vem a foto? A planilha de execução traz link para a foto no GSAN?
