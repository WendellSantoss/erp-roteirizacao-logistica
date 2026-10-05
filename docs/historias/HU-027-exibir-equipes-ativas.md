---
id: HU-027
titulo: Ver quantas equipes estão disponíveis no polo
ordem: 42
modulo: Equipes
epico: EP-B Planejamento e despacho
tela: "Configurações · Equipes" › "N equipes ativas para roteirização"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-EQP-02]
regras: []
nao_funcionais: []
depende_de: [HU-009, HU-054]
---

# HU-027 — Ver quantas equipes estão disponíveis no polo

## História
Como **Coordenador de Campo**, quero **ver quantas equipes ativas tenho no polo**, para **saber
de antemão quantas rotas consigo montar no dia**.

## Critérios de aceite
CA01 — Total do polo
Dado o Polo 1 com 5 equipes ativas e 1 inativa
Quando abro Configurações · Equipes
Então vejo "5 equipes ativas para roteirização".

CA02 — Capacidade somada
Dado as 5 equipes com capacidades 25, 25, 20, 20, 15
Quando olho o resumo
Então vejo também "Capacidade total: 105 OSs/dia".

CA03 — "Todos"
Dado o seletor em "Todos"
Quando abro a tela
Então o total é a soma dos polos do usuário, e os cartões mostram o polo de cada equipe.

CA04 — Atualização
Dado o total 5
Quando inativo uma equipe
Então o total passa a 4 sem recarregar a página.
