---
id: HU-017
titulo: Confirmar o recebimento de uma carga
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › "Recebimentos pendentes" › "Receber carga"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-09]
regras: [RN-12]
nao_funcionais: [RNF-15]
depende_de: [HU-036]
---

# HU-017 — Confirmar o recebimento de uma carga

## História
Como **Almoxarife do polo destino**, quero **confirmar que a carga chegou**, para **que os kits
passem a contar no saldo do meu polo**.

## Regras de negócio
- **RN-12** — Só depois da confirmação a quantidade entra no saldo do destino.
- **RN-L01** — Só o almoxarife do polo destino confirma.
- **RN-L02** — Quantidade recebida igual à enviada → confirmação simples; menor → divergência
  (HU-047); maior → recusado.

## Critérios de aceite
CA01 — Confirmar
Dado uma carga de 20 Hidrômetros do Polo 1 para o Polo 2
Quando o almoxarife do Polo 2 clica em "Receber carga", confere os dados e confirma 20
Então o saldo do Polo 2 aumenta 20, o envio fica "recebido" com data/hora e usuário, e some dos pendentes.

CA02 — Polo errado
Dado a mesma carga
Quando o almoxarife do Polo 1 tenta confirmar pela API
Então recebe `403`.

CA03 — Quantidade maior
Dado a carga de 20
Quando informo 22
Então aparece "Quantidade recebida maior que a enviada (20)" e nada muda.

CA04 — Confirmação dupla
Dado a carga já recebida
Quando duas abas tentam confirmar de novo
Então o saldo só aumenta uma vez.
