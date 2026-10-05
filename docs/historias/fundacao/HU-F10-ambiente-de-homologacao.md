---
id: HU-F10
titulo: Publicar ambiente de homologação
ordem: 10
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-13]
depende_de: [HU-F02, HU-F06]
---

# HU-F10 — Publicar ambiente de homologação

## História
Como **integrante do grupo que não programa com agente**, quero **acessar uma versão do sistema
publicada a cada merge na `main`**, para **testar as histórias concluídas e homologar sem
precisar montar o ambiente local**.

## Critérios de aceite
CA01 — Deploy automático
Dado um merge na `main` com CI verde
Quando o pipeline termina
Então a nova versão está no ar no ambiente de homologação em até 15 min.

CA02 — HTTPS (RNF-13)
Dado o endereço de homologação
Quando acesso por `http://`
Então sou redirecionado para `https://`.

CA03 — Versão visível
Dado o sistema em homologação
Quando abro o rodapé ou `/api/health`
Então vejo o commit publicado.

## Dúvidas em aberto
- Onde hospedar (custo zero ou crédito acadêmico)? Decisão do grupo; pode entrar no ADR.
