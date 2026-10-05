---
id: HU-058
titulo: Marcar uma OS como prioridade
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › pin › "Marcar como prioridade"
fase: 2
prioridade: MVP
status: proposta
requisitos: [RF-ROT-05 (proposto)]
regras: [RN-02]
nao_funcionais: [RNF-15]
depende_de: [HU-012]
---

# HU-058 — Marcar uma OS como prioridade

> **Proposta — validar com o grupo.** A prioridade manual é citada em RF-IMP-04 e RN-02, mas não
> há requisito que a crie.

## História
Como **Coordenador de Campo**, quero **marcar uma OS como prioritária direto no mapa**, para
**garantir que ela entre na rota do dia mesmo que não esteja atrasada**.

## Regras de negócio
- **RN-02** — A prioridade manual sobrevive a reimportações.
- **RN-L01** — Prioridade é sim/não; pode ser marcada e desmarcada até o despacho.
- **RN-L02** — OS prioritária tem destaque no mapa e na lista, e vem primeiro nas ordenações.

## Critérios de aceite
CA01 — Marcar
Dado a OS 4471203 no mapa
Quando clico no pin e em "Marcar como prioridade"
Então o pin ganha o destaque de prioridade, a OS aparece no filtro "Prioritárias" (HU-025) e a
trilha registra autor e data/hora.

CA02 — Desmarcar
Dado a OS prioritária
Quando clico em "Remover prioridade"
Então o destaque some.

CA03 — Sobrevive à importação
Dado a OS prioritária
Quando a planilha do dia seguinte é importada
Então ela continua prioritária.

CA04 — Após despacho
Dado uma OS despachada
Quando abro o pin
Então a ação de prioridade não aparece.
