---
id: HU-057
titulo: Atribuir rapidamente as OSs selecionadas a uma equipe
ordem: 47
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › modal "Atribuir despacho"
fase: 2
prioridade: MVP
status: proposta
requisitos: [RF-ROT-04 (proposto)]
regras: [RN-08, RN-09]
nao_funcionais: [RNF-15]
depende_de: [HU-056]
---

# HU-057 — Atribuir rapidamente as OSs selecionadas a uma equipe

> **Proposta — validar com o grupo.** O protótipo tem o modal "Atribuir despacho" (equipe +
> data) separado de "Criar Rota". Esta história define a diferença entre os dois.

## História
Como **Coordenador de Campo**, quero **mandar as OSs selecionadas para uma equipe em uma data
sem preencher o formulário completo de rota**, para **completar rápido a rota de uma equipe que
já está montada**.

## Regras de negócio
- **RN-L01** — Se a equipe já tem rota na operação e data, as OSs são **acrescentadas** a ela.
- **RN-L02** — Se não tem, é criada uma rota com nome "<Equipe> · <data>" e os demais campos
  obrigatórios ficam pendentes (a rota não deixa finalizar o planejamento até completar, HU-013).
- **RN-L03** — Mesmas validações de capacidade e polo da HU-056.

## Critérios de aceite
CA01 — Acrescentar à rota existente
Dado a Equipe A com a rota "Bessa manhã" (18 OSs, capacidade 25) e 5 OSs selecionadas
Quando atribuo à Equipe A em 12/07
Então a rota passa a ter 23 OSs, e as 5 vão para "Roteirizada".

CA02 — Criar rota mínima
Dado a Equipe C sem rota em 12/07
Quando atribuo 10 OSs
Então é criada a rota "Equipe C · 12/07" com as 10 OSs, marcada "dados incompletos".

CA03 — Capacidade
Dado a Equipe A com 23 de 25
Quando atribuo mais 5
Então é recusado com "Equipe A: 28 OSs no dia excede a capacidade de 25".

## Dúvidas em aberto
- O grupo prefere ter só "Criar Rota" e remover "Atribuir despacho" do protótipo?
