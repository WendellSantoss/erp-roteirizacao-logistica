# Etapa 7 — Integração e testes

**Projeto:** GeniOS — ERP Roteirização Logística  
**Repositório:** [WendellSantoss/erp-roteirizacao-logistica](https://github.com/WendellSantoss/erp-roteirizacao-logistica)  
**Versão final:** integrada à branch `main` pela PR [#93](https://github.com/WendellSantoss/erp-roteirizacao-logistica/pull/93)  
**Data da verificação:** 24/11/2026

## 1. Objetivo

Validar os critérios de aceite do MVP de ponta a ponta, registrar os resultados dos testes disponíveis e identificar eventuais limitações das evidências da versão final.

## 2. Evidências automatizadas

A validação final foi executada no workflow **Qualidade** associado à PR #93:

- **Execução:** [GitHub Actions — Qualidade #15](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45378825497)
- **Commit da entrega:** `7fbb169d97f0327d4b6aa81f3226544d358f26d3`
- **Data:** 24/11/2026
- **Resultado geral:** **sucesso — 3 de 3 jobs concluídos** (backend, frontend e smoke test dos serviços publicados).

### 2.1 Backend

Ambiente de CI: Python 3.13 e PostgreSQL 17.

| Verificação | Resultado |
|---|---|
| Instalação das dependências de desenvolvimento | Aprovado |
| Formatação — `ruff format --check .` | Aprovado |
| Lint — `ruff check .` | Aprovado |
| Regras de dependência entre módulos — `lint-imports` | Aprovado |
| Sincronização das migrations — `makemigrations --check --dry-run` | Aprovado |
| Testes automatizados — `python manage.py test` | **101 testes aprovados** |

O log do job registra: `Ran 101 tests`, seguido de `OK`.

Os testes cobrem os critérios documentados para autenticação e bloqueio de login (HU-019), matriz de permissões e segregação por polo (HU-020), ciclo de vida das Ordens de Serviço (HU-F11), importação e upsert (HU-001 a HU-004), pendências (HU-006 a HU-008) e trava de kits (HU-016).

### 2.2 Frontend

Ambiente de CI: Node.js 22.

| Verificação | Resultado |
|---|---|
| Instalação limpa — `npm ci` | Aprovado |
| Formatação — `npm run format:check` | Aprovado |
| Lint — `npm run lint` | Aprovado |
| Testes — `npm test` | **9 testes aprovados** |
| Build de produção — `npm run build` | Aprovado |

O Vitest executou 2 arquivos de teste: 4 testes em `planilha.test.ts` e 5 em `formatacao.test.ts`. O build TypeScript/Vite foi concluído com sucesso.

## 3. Verificação do health check e integração publicada

O job `Smoke test dos serviços publicados` foi executado e concluído com sucesso na execução #15. O passo `Verificar frontend na Vercel` foi aprovado e o passo `Verificar API e conexão com Neon pelo health check` também foi aprovado. Assim, o runner do GitHub confirmou a resposta do frontend publicado e o endpoint `/health` retornando os estados esperados da API e do banco.

O contrato do endpoint `GET /health` prevê:

- HTTP 200 e resposta `{"status":"API OK","database":"Banco OK"}` quando a consulta ao PostgreSQL funciona;
- HTTP 503 e resposta `{"status":"API OK","database":"Erro no banco"}` quando o banco não está disponível.

Os dois comportamentos possuem testes automatizados em `backend/nucleo/tests/test_health.py`.

**Limitação da evidência automatizada:** a validação publicada foi feita por requisições HTTP automatizadas no runner do GitHub. Esse procedimento comprova a disponibilidade e o contrato do endpoint, mas não substitui a inspeção visual manual da interface nem demonstra, por si só, todos os fluxos de usuário.

URLs previstas no README do projeto:

- Frontend: https://erp-roteirizacao-logistica-so5e.vercel.app
- Health check da API: https://genios-api-kruh.onrender.com/health

## 4. Evidências visuais anexadas

<badge>104 arquivos PNG registrados</badge>

O repositório contém **104 capturas PNG** organizadas por visão geral e perfil de acesso, no diretório [`docs/testes-e-integracao/evidencias/`](https://github.com/WendellSantoss/erp-roteirizacao-logistica/tree/main/docs/testes-e-integracao/evidencias). O inventário e os links individuais estão no [índice de evidências visuais](https://github.com/WendellSantoss/erp-roteirizacao-logistica/blob/main/docs/testes-e-integracao/evidencias/README.md).

| Pasta | Perfil / conteúdo | Capturas |
|---|---|---:|
| `0-geral` | Visão geral do sistema | 6 |
| `1-ana-analista` | Ana — Analista | 26 |
| `2-bruno-analista-polo2` | Bruno — Analista do Polo 2 | 17 |
| `3-carlos-almoxarife` | Carlos — Almoxarife | 9 |
| `4-gabriela-gerente` | Gabriela — Gerente | 22 |
| `5-alice-auditora` | Alice — Auditora | 7 |
| `6-davi-admin` | Davi — Administrador | 17 |
| **Total** | | **104** |

As capturas catalogadas abrangem telas de login, navegação por perfil, permissões e restrições de acesso, pendências, importação, almoxarifado e auditoria. As descrições do índice foram elaboradas a partir dos nomes dos arquivos; por isso, devem ser interpretadas como identificação do assunto indicado pelo nome, não como validação independente de cada resultado visual.

As imagens complementam os logs do CI e os testes automatizados. Não substituem os resultados de execução, nem comprovam isoladamente respostas HTTP ou cenários que não estejam representados na captura.

## 5. Resultado consolidado

| Critério | Situação | Evidência |
|---|---|---|
| Testes automatizados do backend | **Aprovado** | 101 testes no PostgreSQL 17 |
| Testes automatizados do frontend | **Aprovado** | 9 testes no Vitest |
| Qualidade estática e formatação | **Aprovado** | Ruff, import-linter, Prettier e ESLint |
| Migrations sincronizadas | **Aprovado** | Etapa de CI concluída |
| Build de produção do frontend | **Aprovado** | TypeScript e Vite concluídos |
| Health check com banco (teste automatizado) | **Aprovado** | Casos HTTP 200 e HTTP 503 cobertos |
| Smoke test das URLs publicadas (Vercel e Render/Neon) | **Aprovado** | Execução #15: os dois passos do job `Smoke test dos serviços publicados` concluídos com sucesso |
| Capturas visuais organizadas no repositório | **Anexadas** | 104 arquivos PNG catalogados por perfil |

## 6. Conclusão

A execução automatizada registrada no GitHub Actions comprova que a suíte existente passou: **101 testes de backend e 9 testes de frontend**, além das verificações de qualidade, migrations e build.

A integração publicada foi validada com sucesso pelo job de smoke test na execução #15 do GitHub Actions. Os três jobs da execução final (backend, frontend e smoke test) terminaram com sucesso.

Como complemento, o repositório contém **104 capturas PNG**, organizadas por perfil e acompanhadas de índice com links e descrições. As capturas ampliam a rastreabilidade visual dos fluxos documentados, enquanto os logs do CI permanecem como evidência dos testes automatizados e do smoke test.

**Entregável desta etapa:** relatório de testes, resultados automatizados registrados, integração publicada verificada e acervo de evidências visuais anexado e catalogado na branch `main`.
