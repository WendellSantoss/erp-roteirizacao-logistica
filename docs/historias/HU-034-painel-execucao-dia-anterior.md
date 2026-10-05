---
id: HU-034
titulo: Ver a execução de ontem por kit
ordem: 70
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › "Execução de ontem"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-05]
regras: [RN-11]
nao_funcionais: []
depende_de: [HU-016, HU-032]
---

# HU-034 — Ver a execução de ontem por kit

## História
Como **Almoxarife**, quero **ver ao lado do formulário quanto foi executado ontem de cada kit e
quanto ainda posso entregar hoje**, para **planejar as saídas antes de esbarrar na trava**.

## Regras de negócio
- **RN-L01** — Usa exatamente o mesmo cálculo da trava (HU-016): mesmo D−1, mesmo vínculo kit ↔
  serviço, mesmo polo. Painel e trava nunca podem divergir.

## Critérios de aceite
CA01 — Painel
Dado ontem no Polo 1: 10 Hidrômetro, 25 Ligação Simples, 0 Supressão, 4 Religação
Quando abro o Almoxarifado no Polo 1
Então o painel mostra cada kit ativo com "executado ontem" e "disponível hoje".

CA02 — Atualiza com a saída
Dado Hidrômetro com 10 disponíveis
Quando registro saída de 6
Então o painel mostra 4 disponíveis sem recarregar.

CA03 — Sem execução importada
Dado que a planilha de execução de ontem ainda não foi importada
Quando abro o painel
Então aparece o aviso "Execução de ontem ainda não importada — a trava bloqueará todas as saídas".

CA04 — Mesma conta da trava
Dado qualquer cenário de teste da HU-016
Quando comparo o "disponível hoje" do painel com o limite aplicado pela trava
Então são iguais (teste automatizado compartilhado).
