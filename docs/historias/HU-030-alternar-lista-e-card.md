---
id: HU-030
titulo: Alternar entre visualização em lista e em cartões
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › botões "Lista" e "Card"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-ROT-02]
regras: []
nao_funcionais: [RNF-22]
depende_de: [HU-011]
---

# HU-030 — Alternar entre visualização em lista e em cartões

## História
Como **Coordenador de Campo**, quero **ver as OSs em planejamento como lista ou como cartões**,
para **usar a lista para comparar muitas OSs e os cartões para ver detalhes de poucas**.

## Critérios de aceite
CA01 — Alternar
Dado 120 OSs aptas no planejamento
Quando clico em "Card"
Então as mesmas 120 aparecem como cartões, com número da OS, bairro, tipo de serviço, atraso e prioridade.

CA02 — Mesmo conjunto
Dado um filtro aplicado e 5 OSs selecionadas
Quando alterno entre Lista e Card
Então o filtro e a seleção continuam iguais.

CA03 — Lembrar preferência
Dado que escolhi "Card"
Quando volto ao Roteirizador outro dia
Então ele abre em "Card".

CA04 — Selecionar pela lista
Dado a visualização em Lista
Quando marco uma OS
Então ela fica selecionada também no mapa e o contador (HU-031) aumenta.
