---
id: HU-047
titulo: Registrar divergência no recebimento
ordem: 76
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › "Receber carga" (variação ainda não desenhada)
fase: 4
prioridade: desejável
status: rascunho
requisitos: [RF-ALM-10]
regras: [RN-12]
nao_funcionais: [RNF-15]
depende_de: [HU-017]
---

# HU-047 — Registrar divergência no recebimento

## História
Como **Almoxarife do polo destino**, quero **registrar que chegou menos do que foi enviado**,
para **que a diferença seja investigada e o saldo reflita o que realmente está no polo**.

## Regras de negócio
- **RN-L01** — Entra no saldo do destino apenas a quantidade recebida.
- **RN-L02** — A diferença gera uma pendência de conciliação com motivo obrigatório.
- **RN-L03** — A pendência é encerrada pelo Gerente de Contrato com uma resolução (ex.: "extravio",
  "erro de digitação no envio").

## Critérios de aceite
CA01 — Registrar
Dado uma carga de 20 enviada
Quando confirmo 17 com o motivo "3 caixas danificadas"
Então o saldo do destino aumenta 17, o envio fica "recebido com divergência" e é criada uma
pendência de conciliação de 3 unidades.

CA02 — Motivo obrigatório
Dado 17 de 20
Quando confirmo sem motivo
Então aparece "Informe o motivo da divergência".

CA03 — Encerrar
Dado a pendência aberta
Quando o Gerente registra a resolução "extravio"
Então a pendência é encerrada, com autor e data/hora na trilha.
