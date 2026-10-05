---
id: HU-033
titulo: Explicar por que a saída foi bloqueada
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › diálogo "Saída bloqueada"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-04]
regras: [RN-11]
nao_funcionais: [RNF-19]
depende_de: [HU-016]
---

# HU-033 — Explicar por que a saída foi bloqueada

## História
Como **Almoxarife**, quero **ver claramente o kit, quanto pedi e quanto foi executado ontem
quando a saída é bloqueada**, para **ajustar a quantidade sem precisar perguntar a ninguém**.

## Critérios de aceite
CA01 — Diálogo
Dado uma saída bloqueada pela trava (HU-016) de "Kit Hidrômetro" com 11 solicitados hoje e 10
executados ontem
Quando o bloqueio acontece
Então abre o diálogo "Saída bloqueada" com o texto "A quantidade solicitada excede a execução do
dia anterior", e três campos: Kit "Kit Hidrômetro", Solicitado "11 un.", Executado ontem "10 un.".

CA02 — Quanto ainda dá
Dado o CA01 com 6 já entregues hoje
Quando o diálogo abre
Então também mostra "Disponível hoje pela trava: 4 un.".

CA03 — Ajustar
Dado o diálogo aberto
Quando clico em "Entendi, ajustar"
Então o diálogo fecha, o formulário mantém equipe e kit, e o foco vai para a quantidade.

CA04 — Liberação excepcional
Dado um usuário com permissão de liberar a trava (HU-063)
Quando o diálogo abre
Então há também o botão "Solicitar liberação"; para os demais perfis ele não aparece.
