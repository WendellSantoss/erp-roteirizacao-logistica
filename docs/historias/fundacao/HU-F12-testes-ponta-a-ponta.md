---
id: HU-F12
titulo: Rodar testes de ponta a ponta no navegador
ordem: 12
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-23]
depende_de: [HU-F04, HU-F06, HU-F09]
---

# HU-F12 — Rodar testes de ponta a ponta no navegador

## História
Como **grupo do GeniOS**, queremos **testes automatizados que usam o sistema pelo navegador como
um usuário**, para **verificar critérios que só existem na tela (arrastar arquivo, desenhar
polígono, editar na grade) a cada pull request**.

## Critérios de aceite
CA01 — Infraestrutura
Dado o repositório
Quando executo `npm run e2e`
Então o Playwright sobe o ambiente com os dados de exemplo (HU-F09) e roda os testes em
Chromium, Firefox e Edge (RNF-23).

CA02 — Login reutilizável
Dado um teste que precisa de um perfil
Quando ele pede "logado como Almoxarife do Polo 1"
Então o login é feito por um utilitário compartilhado, sem repetir passos em cada teste.

CA03 — No CI
Dado um pull request
Quando o CI roda (HU-F06)
Então os testes de ponta a ponta rodam, e em caso de falha o vídeo e o trace ficam disponíveis
como artefato.

CA04 — Teste de fumaça
Dado o sistema no ar
Quando o teste de fumaça roda
Então ele faz login, troca o polo e abre cada módulo do menu sem erro no console.
