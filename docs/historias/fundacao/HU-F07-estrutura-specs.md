---
id: HU-F07
titulo: Preparar o repositório para desenvolvimento por especificação
ordem: 7
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: []
depende_de: [HU-F01]
---

# HU-F07 — Preparar o repositório para desenvolvimento por especificação

## História
Como **desenvolvedor que usa agente de IA (Claude Code ou Codex)**, quero **instruções do projeto
e um lugar padrão para especificações e planos de cada história**, para **que o agente siga as
regras do GeniOS e o grupo consiga revisar o que foi pedido, planejado e entregue**.

## Contexto
O fluxo é: história (`docs/historias/`) → especificação técnica (`docs/specs/HU-xxx/spec.md`) →
plano de tarefas (`docs/specs/HU-xxx/plano.md`) → implementação → pull request. O processo
completo está em `docs/processo/desenvolvimento-por-especificacao.md`.

## Critérios de aceite
CA01 — Instruções para agentes
Dado a raiz do repositório
Quando abro `AGENTS.md`
Então ele descreve a stack, a estrutura de pastas, os comandos de teste e lint, as regras da
HU-F03 (RN-L01, RN-L02) e a regra "nenhum código sem teste do critério de aceite"; `CLAUDE.md`
apenas importa o `AGENTS.md`, para que Claude Code e Codex leiam as mesmas regras.

CA02 — Modelos de especificação e plano
Dado `docs/specs/_modelos/`
Quando listo
Então existem `spec.md` (objetivo, critérios de aceite copiados da história, modelo de dados,
endpoints, telas, testes, riscos) e `plano.md` (tarefas pequenas, cada uma com arquivos e teste).

CA03 — Exemplo completo
Dado `docs/specs/HU-F03/`
Quando abro
Então existem a spec e o plano usados para construir o esqueleto do backend, servindo de exemplo.

CA04 — Fonte única
Dado o `AGENTS.md`
Quando procuro regras de negócio copiadas da ERS
Então não encontro; ele aponta para `docs/requisitos/ers.md` e `docs/historias/` em vez de duplicar.
