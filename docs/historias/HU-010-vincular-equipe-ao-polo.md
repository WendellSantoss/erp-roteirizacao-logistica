---
id: HU-010
titulo: Restringir cada equipe ao seu polo
modulo: Equipes
epico: EP-B Planejamento e despacho
tela: "Configurações (Equipes)"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-EQP-03]
regras: [RN-09]
nao_funcionais: [RNF-08]
depende_de: [HU-009]
---

# HU-010 — Restringir cada equipe ao seu polo

## História
Como **Administrador**, quero **que cada equipe pertença a um único polo e só possa ser usada em
rotas desse polo**, para **que uma equipe do Norte não seja despachada por engano para o Sul**.

## Regras de negócio
- **RN-09** — A equipe da rota deve ser do polo da OS e estar ativa na data.
- **RN-L01** — Trocar o polo de uma equipe só é permitido sem rotas em aberto.
- **RN-L02** — A regra vale no servidor, para qualquer origem (tela, API, assistente — RN-21).

## Critérios de aceite
CA01 — Polo obrigatório
Dado o cadastro de equipe
Quando salvo sem polo
Então aparece "Informe o polo da equipe".

CA02 — Só equipes do polo
Dado o Roteirizador no Polo 2
Quando abro a lista de equipes para criar rota
Então aparecem só as equipes ativas do Polo 2.

CA03 — Contorno pela API
Dado OSs do Polo 2
Quando envio à API uma rota com equipe do Polo 1
Então recebo `422` "A Equipe A pertence ao Polo 1 e não pode atender o Polo 2".

CA04 — Troca de polo bloqueada
Dado a Equipe B com rota aberta amanhã no Polo 1
Quando tento mudar o polo dela para Polo 3
Então a alteração é recusada com "Equipe com rotas em aberto: <rotas>. Realoque antes de trocar o polo".

CA05 — Troca de polo permitida
Dado a Equipe B sem rotas em aberto
Quando mudo o polo para Polo 3
Então ela passa a aparecer só no Polo 3, e a trilha registra a troca.
