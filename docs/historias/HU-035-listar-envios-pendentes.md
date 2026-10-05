---
id: HU-035
titulo: Acompanhar os envios de kits para outros polos
ordem: 73
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › "Envios pendentes"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-07]
regras: [RN-12]
nao_funcionais: [RNF-20]
depende_de: [HU-067]
---

# HU-035 — Acompanhar os envios de kits para outros polos

## História
Como **Almoxarife**, quero **ver os envios que saíram do meu polo e ainda não foram recebidos**,
para **cobrar o polo destino quando algo demorar**.

## Critérios de aceite
CA01 — Lista
Dado 3 envios do Polo 1 em trânsito
Quando abro "Envios pendentes" no Polo 1
Então vejo o contador "3" e, para cada envio: kit, status "em trânsito", destino, equipe,
quantidade e data/hora de envio.

CA02 — Sai ao ser recebido
Dado um envio para o Polo 2
Quando o Polo 2 confirma o recebimento (HU-017)
Então ele sai da lista e o contador diminui.

CA03 — Com divergência
Dado um envio recebido com divergência (HU-047)
Quando olho a lista
Então ele aparece com status "divergência" até a conciliação.

CA04 — Vazio
Dado nenhum envio pendente
Quando abro
Então vejo "Nenhum envio pendente".
