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

## 5. Matriz de rastreabilidade — histórias prioritárias x testes ponta a ponta

A matriz abaixo relaciona as cinco histórias priorizadas em `docs/historias-priorizadas.md` aos cenários que devem ser demonstrados, ao resultado documentado e às evidências disponíveis. Ela separa testes automatizados de backend, testes unitários do frontend, roteiro Playwright local e capturas de tela. Uma captura comprova apenas o estado visual que apresenta; não substitui log de execução ou teste automatizado.

| História prioritária | Cenários de validação ponta a ponta | Resultado documentado | Evidências disponíveis |
|---|---|---|---|
| **1. Acesso e filtro global por polo (HU-019 e HU-020)** | Realizar login individual; exibir nome e perfil; selecionar um polo; tentar acessar dados de outro polo; confirmar bloqueio de ações de escrita quando `Todos` estiver selecionado; verificar restrições por perfil. | **Backend: aprovado na suíte automatizada.** O relatório da suíte registra cobertura de autenticação, bloqueio de login, matriz de permissões e segregação por polo. **Frontend: roteiro Playwright local reportado como aprovado** no registro de uso de IA. O smoke test publicado não percorre login nem permissões. | [CI — job backend](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45378825497); [login](evidencias/0-geral/01-login.png), [credenciais inválidas](evidencias/0-geral/02-login-credenciais-invalidas.png), [login bloqueado](evidencias/0-geral/03-login-bloqueado-5-tentativas.png), [analista sem acesso ao almoxarifado](evidencias/1-ana-analista/07-almoxarifado-sem-acesso.png), [analista do Polo 2](evidencias/2-bruno-analista-polo2/02-pendencias.png). |
| **2. Upload, validação de layout e filtro de escopo GSAN (HU-001, HU-002 e HU-003)** | Enviar arquivo `.xlsx` válido; rejeitar formato inválido; rejeitar planilha sem colunas obrigatórias; filtrar OSs fora do escopo; conferir resumo e hash da importação. | **Backend: aprovado na suíte automatizada**, conforme cobertura de importação e validação registrada. **Frontend: 9 testes aprovados**, mas os testes Vitest listados neste relatório cobrem `planilha.test.ts` e `formatacao.test.ts`; não são, isoladamente, prova de fluxo publicado. O roteiro Playwright local das cinco histórias foi reportado como aprovado no registro de IA. | [CI — job backend e frontend](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45378825497); [importação com alertas](evidencias/1-ana-analista/20-importacao-resultado-com-alertas.png), [fora de escopo](evidencias/1-ana-analista/23-importacao-fora-de-escopo.png), [colunas ausentes](evidencias/1-ana-analista/24-importacao-colunas-ausentes.png), [formato inválido](evidencias/1-ana-analista/25-importacao-formato-invalido.png). |
| **3. Importação transacional com upsert sem amnésia (HU-004)** | Importar OSs novas; reimportar OSs existentes; confirmar preservação de prioridade e equipe atribuída manualmente; confirmar preservação de estado terminal e de OSs ausentes no arquivo; verificar rollback em falha; reimportar o mesmo arquivo sem duplicação. | **Backend: aprovado na suíte automatizada**, que o relatório declara cobrir importação e upsert (HU-001 a HU-004). O registro de IA também relata teste de até 5.000 linhas em 1,3 s. **Roteiro Playwright local reportado como aprovado**, sem log Playwright anexado aqui. | [CI — job backend](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45378825497); [mesmo arquivo novamente](evidencias/1-ana-analista/21-importacao-mesmo-arquivo-novamente.png), [resultado de upsert](evidencias/1-ana-analista/22-importacao-atualizacao-upsert.png), [resultado com alertas](evidencias/1-ana-analista/20-importacao-resultado-com-alertas.png); [registro de uso de IA](../registro-uso-ia.md). |
| **4. Listagem e tratamento de pendências de OS (HU-006, HU-007 e HU-008)** | Listar OSs por polo; conferir colunas e contadores; filtrar pendências e atrasos; pesquisar; marcar e retirar prioridade; desconsiderar OS com justificativa; conferir estado terminal e registro correspondente na auditoria. | **Backend: aprovado na suíte automatizada**, conforme cobertura de pendências declarada para HU-006 a HU-008. As capturas catalogam os estados e ações da interface. O roteiro Playwright local das cinco histórias foi reportado como aprovado no registro de IA; não há log de execução anexado a este relatório. | [CI — job backend](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45378825497); [lista de pendências](evidencias/1-ana-analista/02-pendencias-todos-os-polos.png), [filtro de atraso](evidencias/1-ana-analista/11-pendencias-so-em-atraso.png), [prioridade](evidencias/1-ana-analista/15-pendencias-os-priorizada.png), [desconsideração](evidencias/1-ana-analista/19-pendencias-os-desconsiderada.png), [auditoria](evidencias/4-gabriela-gerente/09-auditoria-todos-os-polos.png). |
| **5. Bloqueio de saída de kit por trava de histórico (HU-016)** | Consultar equipes e limites; registrar saída dentro do limite; tentar exceder o executado em D-1; conferir mensagem de bloqueio; verificar que a saída excedente não foi registrada e que a tentativa foi auditada. | **Backend: aprovado na suíte automatizada**, conforme cobertura de trava de kits (HU-016) declarada no relatório. As capturas catalogam saída registrada e bloqueada. O roteiro Playwright local das cinco histórias foi reportado como aprovado no registro de IA; não há log Playwright anexado a este relatório. | [CI — job backend](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45378825497); [almoxarifado](evidencias/3-carlos-almoxarife/04-almoxarifado.png), [saída registrada](evidencias/3-carlos-almoxarife/07-almoxarifado-saida-registrada.png), [saída bloqueada](evidencias/3-carlos-almoxarife/08-almoxarifado-saida-bloqueada.png), [estado após bloqueio](evidencias/3-carlos-almoxarife/09-almoxarifado-apos-bloqueio.png). |

### Limites e interpretação dos resultados

- Os **101 testes de backend** passaram no CI e o relatório declara que cobrem os critérios associados às histórias listadas. A matriz não inventa nomes ou identificadores de testes individuais que não estejam discriminados no log resumido.
- Os **9 testes de frontend** passaram, mas são testes de planilha e formatação; não devem ser apresentados como nove testes completos de interface ou como prova de todos os fluxos de usuário.
- O arquivo `docs/registro-uso-ia.md` relata que um roteiro Playwright local percorreu os fluxos das cinco histórias. Esse resultado está registrado como relato de execução local; para torná-lo reproduzível, anexem o roteiro, o comando utilizado e o log/relatório Playwright, se esses artefatos estiverem disponíveis.
- O smoke test da execução #15 comprova a disponibilidade do frontend publicado e o `GET /health` com conexão ao Neon. Ele **não comprova** login, importação, permissões, tratamento de pendências ou saída de kits na produção.
- Para afirmar que cada história foi validada na URL publicada, executem os cenários da matriz no ambiente publicado e registrem data, ambiente, perfil de usuário, resultado observado e link para a evidência. Até essa execução, mantenham a distinção entre teste automatizado, roteiro local e smoke test de produção.

## 6. Resultado consolidado

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
