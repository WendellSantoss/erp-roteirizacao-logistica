---
id: HU-067
titulo: Registrar envio de kits para outro polo
ordem: 72
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" (formulário de envio a desenhar)
fase: 4
prioridade: MVP
status: proposta
requisitos: [RF-ALM-11 (proposto)]
regras: [RN-12]
nao_funcionais: [RNF-15]
depende_de: [HU-032]
---

# HU-067 — Registrar envio de kits para outro polo

> **Proposta — validar com o grupo.** RF-ALM-07 lista envios pendentes, mas nenhum requisito cria um envio.

## História
Como **Almoxarife**, quero **registrar a remessa de kits do meu polo para outro**, para **que o
outro polo saiba o que vai chegar e o saldo dos dois fique certo**.

## Regras de negócio
- **RN-L01** — Campos: kit, quantidade (≥ 1, ≤ saldo da origem), polo destino (≠ origem),
  equipe responsável pelo transporte (opcional).
- **RN-L02** — O saldo da origem diminui no envio; o do destino só aumenta no recebimento (RN-12).
- **RN-L03** — O envio nasce "em trânsito".

## Critérios de aceite
CA01 — Enviar
Dado saldo de 50 Hidrômetros no Polo 1
Quando envio 20 para o Polo 2
Então o saldo do Polo 1 passa a 30, o envio aparece em "Envios pendentes" do Polo 1 e em
"Recebimentos pendentes" do Polo 2.

CA02 — Mesmo polo
Dado a origem Polo 1
Quando escolho destino Polo 1
Então aparece "O destino deve ser outro polo".

CA03 — Saldo
Dado saldo de 10
Quando envio 20
Então aparece "Saldo insuficiente".
