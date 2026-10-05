---
id: HU-F05
titulo: Publicar o contrato da API
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

# HU-F05 — Publicar o contrato da API

## História
Como **desenvolvedor do GeniOS**, quero **que o contrato OpenAPI seja gerado do backend e que o
frontend use um cliente tipado gerado desse contrato**, para **que uma mudança na API que quebre
o frontend seja detectada na compilação e não em produção**.

## Critérios de aceite
CA01 — Contrato gerado
Dado o backend
Quando executo o comando de geração documentado
Então `docs/api/openapi.yaml` é atualizado e a documentação navegável abre em `/api/docs`.

CA02 — Cliente tipado
Dado o `openapi.yaml`
Quando executo `npm run gen:api` no frontend
Então os tipos e funções de chamada são gerados em `frontend/src/api/`, sem edição manual.

CA03 — Contrato desatualizado quebra o CI
Dado um pull request que altera um endpoint sem regenerar o `openapi.yaml`
Quando o CI roda (HU-F06)
Então a etapa de contrato falha apontando a diferença.
