---
id: HU-029
titulo: Impedir a inativação de equipe com rota em aberto
ordem: 46
modulo: Equipes
epico: EP-B Planejamento e despacho
tela: "Configurações (Equipes)" › "Editar"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-EQP-05]
regras: [RN-09]
nao_funcionais: [RNF-19]
depende_de: [HU-009, HU-056]
---

# HU-029 — Impedir a inativação de equipe com rota em aberto

## História
Como **Administrador**, quero **ser impedido de inativar uma equipe que ainda tem rota a
cumprir**, para **que nenhuma rota fique sem equipe**.

## Regras de negócio
- **RN-L01** — Rota em aberto: rota com data de hoje ou futura cujas OSs ainda não foram despachadas.

## Critérios de aceite
CA01 — Bloqueio
Dado a Equipe A com a rota "Bessa manhã" amanhã, não despachada
Quando tento inativar a Equipe A
Então a inativação é recusada com "A Equipe A tem 1 rota em aberto: Bessa manhã (12/07). Realoque
as OSs para outra equipe antes de inativar", com link para a rota.

CA02 — Rota já despachada não bloqueia
Dado a Equipe A com rota de hoje já despachada (RPA gerado)
Quando inativo
Então a inativação é aceita.

CA03 — Rota passada não bloqueia
Dado a Equipe A com uma rota de ontem não despachada
Quando inativo
Então a inativação é aceita (a rota de ontem é histórico).

CA04 — Pela API
Dado o CA01
Quando envio a inativação direto à API
Então recebo `422` com o mesmo motivo.
