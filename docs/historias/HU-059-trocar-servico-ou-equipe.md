---
id: HU-059
titulo: Trocar a equipe ou retirar uma OS da rota antes do despacho
ordem: 51
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › pin › "Trocar serviço / equipe"
fase: 2
prioridade: MVP
status: proposta
requisitos: [RF-ROT-06 (proposto)]
regras: [RN-09, RN-10]
nao_funcionais: [RNF-15]
depende_de: [HU-056]
---

# HU-059 — Trocar a equipe ou retirar uma OS da rota antes do despacho

> **Proposta — validar com o grupo.** RN-10 bloqueia edições só **depois** do RPA, o que implica
> que antes elas são permitidas; não havia requisito para isso.

## História
Como **Coordenador de Campo**, quero **mover uma OS de uma rota para outra ou devolvê-la para a
fila**, para **corrigir o planejamento até o momento do despacho**.

## Regras de negócio
- **RN-L01** — Mover para outra rota do mesmo planejamento: valida polo e capacidade da equipe destino.
- **RN-L02** — Retirar da rota: a OS volta a "Apta a roteirizar".
- **RN-L03** — Só antes da finalização do planejamento (HU-013) e do RPA (RN-10).

## Critérios de aceite
CA01 — Mover
Dado a OS 4471203 na rota da Equipe A
Quando escolho "Trocar equipe" e seleciono a rota da Equipe B
Então a OS sai da rota A e entra na rota B; a trilha registra a troca.

CA02 — Retirar
Dado a OS na rota da Equipe A
Quando escolho "Retirar da rota"
Então ela volta a "Apta a roteirizar" e aparece de novo como pin livre.

CA03 — Capacidade da destino
Dado a Equipe B com 25 de 25
Quando tento mover uma OS para ela
Então é recusado com o aviso de capacidade.

CA04 — Depois de finalizar
Dado o planejamento finalizado
Quando abro o pin
Então "Trocar equipe" e "Retirar da rota" estão desabilitados.

## Dúvidas em aberto
- O que é "trocar serviço" no protótipo? Mudar o tipo de serviço da OS altera o valor (RN-16) e
  o kit necessário — o Coordenador pode fazer isso, ou só o GSAN?
