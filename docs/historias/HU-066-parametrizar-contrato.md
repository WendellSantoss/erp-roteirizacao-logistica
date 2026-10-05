---
id: HU-066
titulo: Parametrizar preços, prazos, unidades do escopo e operações
ordem: 23
modulo: Transversal
epico: EP-F Requisitos transversais
tela: — (a desenhar)
fase: 1
prioridade: MVP
status: proposta
requisitos: [RF-TRV-07 (proposto)]
regras: [RN-06, RN-11, RN-16]
nao_funcionais: [RNF-26, RNF-27, RNF-15]
depende_de: [HU-020, HU-F11]
---

# HU-066 — Parametrizar preços, prazos, unidades do escopo e operações

> **Proposta — validar com o grupo.** RNF-27 exige que esses catálogos sejam parametrizáveis,
> e várias histórias dependem deles (HU-003, HU-008, HU-011, HU-018, HU-016), mas não há requisito.

## História
Como **Administrador**, quero **manter os parâmetros do contrato no próprio sistema**, para **que
uma mudança de preço, prazo ou escopo não exija nova versão do software (RNF-27)**.

## Regras de negócio
- **RN-L01** — Tipos de serviço: nome, prazo contratual em horas, preço unitário.
- **RN-L02** — Preço e prazo têm **vigência** (data de início). Mudança cria nova vigência; a
  anterior é mantida para recalcular o passado corretamente (RN-16).
- **RN-L03** — Unidades: código GSAN, nome, polo, se está no escopo do contrato.
- **RN-L04** — Operações: nome (PSS, XPT Express, Litoral) e status.
- **RN-L05** — Toda mudança vai para a trilha.

## Critérios de aceite
CA01 — Nova vigência de preço
Dado "Ligação Simples" a R$ 250,00 desde 01/01/2026
Quando cadastro R$ 270,00 a partir de 01/08/2026
Então OSs executadas até 31/07 valem R$ 250,00 e a partir de 01/08 valem R$ 270,00.

CA02 — Escopo
Dado a unidade "Jardim Novo" fora do escopo
Quando marco como "no escopo" do Polo 2
Então a próxima importação do Polo 2 passa a aceitar as OSs dela.

CA03 — Prazo
Dado "Religação" com prazo 24 h
Quando altero para 12 h a partir de amanhã
Então o atraso de OSs abertas a partir de amanhã usa 12 h.

CA04 — Vigência retroativa
Dado um ciclo fechado em julho
Quando tento criar vigência de preço começando em 15/07
Então é recusado com "Período com ciclo fechado — reabra o ciclo antes".

## Dúvidas em aberto
- O preço depende só do tipo de serviço, ou também do polo/operação?
