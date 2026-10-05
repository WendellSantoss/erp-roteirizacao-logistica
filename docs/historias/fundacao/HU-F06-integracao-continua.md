---
id: HU-F06
titulo: Bloquear merge sem CI verde
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: []
depende_de: [HU-F03, HU-F04]
---

# HU-F06 — Bloquear merge sem CI verde

## História
Como **grupo do GeniOS**, queremos **que todo pull request rode lint, testes e build
automaticamente e só possa entrar na `main` com tudo verde**, para **que código gerado por IA
não quebre o que já funciona sem ninguém perceber**.

## Critérios de aceite
CA01 — Pipeline no pull request
Dado um pull request aberto para `main`
Quando o GitHub Actions executa
Então rodam, em paralelo, lint + testes do backend (com PostgreSQL/PostGIS) e lint + typecheck +
testes + build do frontend, em até 10 min.

CA02 — Merge bloqueado
Dado um pull request com qualquer etapa falhando
Quando tento fazer merge
Então o GitHub impede o merge.

CA03 — Cobertura visível
Dado o pipeline concluído
Quando abro o resumo
Então vejo o percentual de cobertura de testes do backend e do frontend.

CA04 — Rastreabilidade
Dado um pull request cujo título ou descrição não cita nenhuma `HU-`
Quando o CI roda
Então a etapa de verificação falha com a mensagem "PR sem história vinculada".
