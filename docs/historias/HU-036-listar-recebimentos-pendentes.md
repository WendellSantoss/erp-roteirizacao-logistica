---
id: HU-036
titulo: Ver as cargas a receber no meu polo
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › "Recebimentos pendentes"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-08]
regras: [RN-12]
nao_funcionais: [RNF-20]
depende_de: [HU-067]
---

# HU-036 — Ver as cargas a receber no meu polo

## História
Como **Almoxarife**, quero **ver as cargas enviadas para o meu polo que ainda estão em trânsito**,
para **conferir quando chegarem**.

## Critérios de aceite
CA01 — Lista
Dado 2 envios do Polo 1 para o Polo 2
Quando abro "Recebimentos pendentes" no Polo 2
Então vejo o contador "2" e, para cada um: kit, quantidade, "Origem: Polo 1 · em trânsito" e o
botão "Receber carga".

CA02 — Não entra no saldo
Dado uma carga em trânsito de 20 Hidrômetros
Quando olho o saldo do Polo 2
Então os 20 **não** estão somados (RN-12).

CA03 — Vazio
Dado nenhuma carga em trânsito para o polo
Quando abro
Então vejo "Nenhuma carga em trânsito".
