---
id: HU-F01
titulo: Montar o monorepo
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: []
depende_de: []
---

# HU-F01 — Montar o monorepo

## História
Como **desenvolvedor do GeniOS**, quero **um único repositório com backend, frontend e
documentação organizados e com convenções escritas**, para **que qualquer pessoa do grupo (ou
agente de IA) saiba onde cada coisa fica e como contribuir sem perguntar**.

## Contexto
Hoje o repositório tem apenas um `README.md` genérico, que descreve outro domínio (frota,
motoristas, entregas). O grupo decidiu por monorepo: uma especificação costuma tocar backend e
frontend ao mesmo tempo, e o pull request de uma história fica inteiro em um lugar.

## Regras
- **RN-L01** — Estrutura de pastas na raiz: `backend/`, `frontend/`, `docs/`, `infra/`.
- **RN-L02** — Branches: `main` protegida; trabalho em `hu-<id>-<slug>` (ex.: `hu-016-trava-historico`).
- **RN-L03** — Commits no padrão Conventional Commits, citando a história no rodapé
  (`Refs: HU-016`).
- **RN-L04** — Todo pull request usa o template e aponta a história que implementa.

## Critérios de aceite
CA01 — Estrutura criada
Dado o repositório clonado
Quando listo a raiz
Então existem `backend/`, `frontend/`, `docs/`, `infra/`, `README.md`, `CONTRIBUTING.md`,
`.gitignore` e `.editorconfig`.

CA02 — README reflete o GeniOS
Dado o `README.md`
Quando leio as seções de visão geral, perfis e modelo de dados
Então descrevem o domínio da ERS (OSs, GSAN, polos, kits, BM) e não citam frota, motoristas ou
entregas; o README aponta para `docs/requisitos/ers.md` e `docs/historias/`.

CA03 — Convenções escritas
Dado o `CONTRIBUTING.md`
Quando procuro como nomear branch, escrever commit e abrir pull request
Então as regras RN-L02 a RN-L04 estão descritas com um exemplo cada.

CA04 — Templates do GitHub
Dado que abro uma issue ou um pull request no GitHub
Quando o formulário aparece
Então ele vem pré-preenchido com o template de `.github/` (issue de história; PR com
"História", "Critérios cobertos" e "Como testar").

CA05 — `main` protegida
Dado um push direto para `main`
Quando o GitHub processa o push
Então ele é recusado; a mudança só entra por pull request com 1 aprovação.

## Fora de escopo
Ambiente Docker (HU-F02), esqueletos de código (HU-F03, HU-F04), CI (HU-F06).

## Dúvidas em aberto
- O repositório é do Wendell; a proteção de branch (CA05) precisa ser configurada por ele.
