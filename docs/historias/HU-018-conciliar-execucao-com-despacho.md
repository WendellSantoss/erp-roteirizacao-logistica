---
id: HU-018
titulo: Conciliar a execução com as OSs despachadas
ordem: 53
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › "Grade de auditoria" e "Invalidações"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-AUD-02]
regras: [RN-14, RN-16]
nao_funcionais: [RNF-07, RNF-17]
depende_de: [HU-037, HU-014, HU-F11, HU-066]
---

# HU-018 — Conciliar a execução com as OSs despachadas

## História
Como **Auditor / Faturista**, quero **que o sistema cruze automaticamente a planilha de execução
com as OSs despachadas**, para **ver de uma vez o que foi executado, o que foi reprovado e o que
não bate**.

## Regras de negócio
- **RN-L01** — Correspondência pela chave da OS (número + polo, RN-01).
- **RN-L02** — OS despachada com execução aprovada pela fiscalização → "Executada".
- **RN-L03** — OS despachada com reprovação da fiscalização → "Invalidada", com motivo,
  inspetor e data vindos da planilha.
- **RN-L04** — Linha da planilha sem OS despachada correspondente → divergência "sem
  correspondência" (não muda nenhuma OS).
- **RN-L05** — OS despachada que não aparece na planilha → continua "Despachada" e entra na
  lista "não retornadas".
- **RN-L06** — O valor da OS é calculado pelo tipo de serviço e tabela de preços vigente na data
  de execução (RN-16).

## Critérios de aceite
CA01 — Conciliação
Dado 100 OSs despachadas e uma planilha com 95 linhas: 80 aprovadas, 12 reprovadas e 3 de OSs
não despachadas
Quando a conciliação termina
Então 80 OSs ficam "Executada" com valor, 12 "Invalidada" com motivo, 3 divergências "sem
correspondência", 8 "não retornadas", e um resumo mostra esses números.

CA02 — Sem correspondência
Dado a linha da OS 9990001, que nunca foi despachada
Quando a conciliação termina
Então nenhuma OS muda e a divergência mostra a linha, o número e o motivo.

CA03 — Tudo ou nada
Dado uma falha no meio da conciliação
Quando ela falha
Então nenhuma OS mudou de estado.

CA04 — Rastreável
Dado uma OS "Executada"
Quando abro o detalhe
Então vejo de qual planilha de execução e linha veio a mudança.

## Dúvidas em aberto
- **Bloqueante:** como a planilha de execução indica aprovação/reprovação da fiscalização?
  (coluna, valores possíveis). Precisamos de uma planilha real anonimizada.
