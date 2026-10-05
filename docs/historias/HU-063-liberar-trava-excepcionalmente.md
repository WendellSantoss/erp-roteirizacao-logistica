---
id: HU-063
titulo: Liberar excepcionalmente a trava de histórico
ordem: 71
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › diálogo "Saída bloqueada" › "Solicitar liberação" (a desenhar)
fase: 4
prioridade: MVP
status: proposta
requisitos: [RF-ALM-06 (proposto)]
regras: [RN-11, RN-13]
nao_funcionais: [RNF-08, RNF-12, RNF-15]
depende_de: [HU-016, HU-033]
---

# HU-063 — Liberar excepcionalmente a trava de histórico

> **Proposta — validar com o grupo.** RN-13 e RNF-12 citam a liberação da trava, mas não há
> requisito que a descreva. O número RF-ALM-06 está vago na ERS.

## História
Como **Gerente de Contrato**, quero **autorizar uma saída acima do limite da trava, com
justificativa**, para **atender um dia atípico (mutirão, emergência) sem desligar o controle**.

## Regras de negócio
- **RN-13** — Toda liberação registra autor, justificativa e data/hora.
- **RN-L01** — Só o Gerente de Contrato libera (proposta).
- **RN-L02** — A liberação vale para **uma** saída específica (kit, equipe, quantidade, dia), não
  desliga a trava.
- **RN-L03** — Justificativa com pelo menos 20 caracteres.

## Critérios de aceite
CA01 — Liberar
Dado uma saída bloqueada de 15 Hidrômetros com limite 10
Quando o Gerente autoriza com "Mutirão de troca de hidrômetros no Bessa"
Então a saída de 15 é registrada, e a trilha mostra a liberação com autor, justificativa,
limite (10) e quantidade liberada (15).

CA02 — Não desliga a trava
Dado a liberação do CA01
Quando o almoxarife registra mais 1 Hidrômetro no mesmo dia
Então a trava bloqueia normalmente.

CA03 — Sem permissão
Dado um Almoxarife
Quando chama a API de liberação
Então recebe `403`.

CA04 — Justificativa curta
Dado a justificativa "urgente"
Quando o Gerente confirma
Então aparece "Justificativa com pelo menos 20 caracteres".

## Dúvidas em aberto
- A liberação é feita pelo Gerente na tela do almoxarife (presencial) ou é uma solicitação que
  o Gerente aprova depois, de outro lugar?
