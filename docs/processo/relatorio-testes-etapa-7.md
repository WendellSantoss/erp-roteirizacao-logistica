# Etapa 7 — Integração e testes

**Projeto:** GeniOS — ERP Roteirização Logística  
**Repositório:** [WendellSantoss/erp-roteirizacao-logistica](https://github.com/WendellSantoss/erp-roteirizacao-logistica)  
**Branch desta entrega:** `docs/etapa-7-integracao-testes`  
**Data da verificação:** 24/11/2026

## 1. Objetivo

Validar os critérios de aceite do MVP de ponta a ponta, registrar os resultados dos testes disponíveis e identificar eventuais pendências para a versão final.

## 2. Evidências automatizadas

Foi consultada a execução mais recente do workflow **Qualidade** disponível na branch `main` antes desta entrega:

- **Execução:** [GitHub Actions — Qualidade #14](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45166789298)
- **Commit testado:** `38f08bcdf1aec322a8c84b04c5d274039878e8e0`
- **Data da execução:** 23/11/2026
- **Resultado geral:** sucesso — os jobs de backend e frontend foram concluídos.

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

Foi adicionada ao workflow `Qualidade` a etapa `smoke-publicado`, que verifica a resposta HTTP do frontend na Vercel e consulta `/health` no Render, exigindo `API OK` e `Banco OK`. A execução desta etapa na branch desta entrega é a evidência automatizada da integração publicada; o resultado será registrado após a conclusão do workflow.

O contrato do endpoint `GET /health` prevê:

- HTTP 200 e resposta `{"status":"API OK","database":"Banco OK"}` quando a consulta ao PostgreSQL funciona;
- HTTP 503 e resposta `{"status":"API OK","database":"Erro no banco"}` quando o banco não está disponível.

Os dois comportamentos possuem testes automatizados em `backend/nucleo/tests/test_health.py`.

**Limitação desta sessão:** o ambiente de execução desta tarefa não conseguiu resolver os domínios públicos por DNS. Para não depender desse acesso, a verificação foi incorporada ao GitHub Actions e será executada por um runner hospedado do GitHub. A captura visual da interface não é produzida pelo workflow; não serão anexadas imagens simuladas.

URLs previstas no README do projeto:

- Frontend: https://erp-roteirizacao-logistica-so5e.vercel.app
- Health check da API: https://genios-api-kruh.onrender.com/health

### Evidência visual complementar

O workflow automatiza as verificações HTTP e do contrato de saúde. Uma captura visual do navegador pode ser anexada como evidência complementar, mas não será apresentada como realizada sem captura real.

### Roteiro de confirmação manual pendente

1. Abrir a URL do frontend e aguardar a inicialização da aplicação.
2. Confirmar que a interface apresenta **“API OK · Banco OK”** (ou a indicação equivalente prevista na implementação).
3. Abrir diretamente a URL `/health` do Render e confirmar HTTP 200 com `API OK` e `Banco OK`.
4. Registrar captura de tela da interface e da resposta do health check, com data e hora, como evidência da integração publicada.

## 4. Resultado consolidado

| Critério | Situação | Evidência |
|---|---|---|
| Testes automatizados do backend | **Aprovado** | 101 testes no PostgreSQL 17 |
| Testes automatizados do frontend | **Aprovado** | 9 testes no Vitest |
| Qualidade estática e formatação | **Aprovado** | Ruff, import-linter, Prettier e ESLint |
| Migrations sincronizadas | **Aprovado** | Etapa de CI concluída |
| Build de produção do frontend | **Aprovado** | TypeScript e Vite concluídos |
| Health check com banco (teste automatizado) | **Aprovado** | Casos HTTP 200 e HTTP 503 cobertos |
| Smoke test das URLs publicadas (Vercel e Render/Neon) | **Aguardando CI da branch** | Job `smoke-publicado` adicionado ao workflow |
| Captura visual do frontend | **Não capturada** | Não há navegador/sessão visual disponível neste ambiente |

## 5. Conclusão

A execução automatizada registrada no GitHub Actions comprova que a suíte existente passou: **101 testes de backend e 9 testes de frontend**, além das verificações de qualidade, migrations e build.

A etapa de integração publicada será avaliada pelo novo job `smoke-publicado` executado em runner externo do GitHub. Até o encerramento desse job, o resultado permanece aguardando. A captura visual complementar não foi realizada nesta sessão e não é substituída por imagens fictícias.

**Entregável desta etapa:** relatório de testes e workflow com smoke test dos serviços publicados, na branch de entrega. A branch principal não foi alterada.
