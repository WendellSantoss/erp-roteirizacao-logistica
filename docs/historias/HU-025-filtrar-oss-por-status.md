---
id: HU-025
titulo: Filtrar as pendências por situação com contador
ordem: 33
modulo: Pendências
epico: EP-A Ingestão e preparação de dados
tela: "Gerenciar Pendências" › filtros rápidos
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-PEN-02]
regras: []
nao_funcionais: [RNF-02, RNF-22]
depende_de: [HU-006, HU-008]
---

# HU-025 — Filtrar as pendências por situação com contador

## História
Como **Analista de Operações**, quero **filtros de um clique, cada um com a quantidade de OSs**,
para **atacar primeiro o grupo de pendências mais crítico**.

## Regras de negócio
- **RN-L01** — Filtros: Todas, Em atraso, Vence em até 4 h, Sem coordenada, Prioritárias.
  *(proposta — ver dúvidas)*
- **RN-L02** — Os contadores respeitam o polo selecionado e são recalculados a cada mudança na lista.
- **RN-L03** — Um filtro ativo por vez; o filtro escolhido é mantido ao voltar para a tela.

## Critérios de aceite
CA01 — Contadores
Dado 312 pendentes no Polo 1, 40 em atraso, 15 vencendo, 22 sem coordenada e 8 prioritárias
Quando abro a tela
Então vejo "Todas 312", "Em atraso 40", "Vence em até 4 h 15", "Sem coordenada 22", "Prioritárias 8".

CA02 — Filtrar
Dado o CA01
Quando clico em "Sem coordenada"
Então a lista mostra só as 22, e o filtro fica destacado.

CA03 — Contador atualiza
Dado o filtro "Sem coordenada" com 22
Quando informo a coordenada de uma unidade com 3 OSs (HU-024)
Então o contador passa a 19 sem recarregar a página.

CA04 — Filtro vazio
Dado o filtro "Prioritárias" com 0
Quando clico nele
Então vejo o estado vazio "Nenhuma pendência neste filtro".

## Dúvidas em aberto
- A ERS fala em "filtros por status", mas todas as OSs da lista estão no mesmo estado
  ("Pendente"). Os filtros propostos são por situação. O grupo confirma?
