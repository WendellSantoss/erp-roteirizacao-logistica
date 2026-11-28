# Registro de IA

* **Sistema:** GeniOS — ERP Operacional para Roteirização, Controle Logístico e Auditoria de Contratos
* **Repositório no GitHub:** https://github.com/WendellSantoss/erp-roteirizacao-logistica
* **Ferramenta de IA utilizada:** Gemini (Plano Gratuito)
* **Etapa documentada:** Etapa 1 — Pacote de Contexto para a IA

---

## 1. Contextualização do Pacote de Contexto (Etapa 1)

Na **Etapa 1**, a equipe organizou toda a documentação arquitetural e de requisitos do **GeniOS** dentro da pasta `/docs` do repositório [https://github.com/WendellSantoss/erp-roteirizacao-logistica](https://github.com/WendellSantoss/erp-roteirizacao-logistica), criando a base de conhecimento necessária para orientar a geração de código nas etapas seguintes:

* **`docs/historias-priorizadas.md`:** Recorte de 5 histórias de usuário prioritárias (*must have*) alinhadas à Fase 1 (Fundação) da ERS (`HU-019`/`HU-020` de autenticação e filtro global por polo; `HU-001` a `HU-003` de upload, validação e filtro de escopo da planilha GSAN; `HU-004` de importação transacional com upsert sem amnésia; `HU-006` a `HU-008` de listagem e tratamento de pendências; e `HU-016` de trava de histórico na saída de kits).
* **`docs/adr/ADR-001-arquitetura-mvp.md`:** Registro da decisão arquitetural pelo **Monólito Modular** (Python, Django + DRF, PostgreSQL e React + TypeScript), justificando a escolha frente aos atributos de integridade, segurança das regras no servidor e auditabilidade.
* **`docs/diagramas-c4/`:** Diagramas arquiteturais exportados em `.jpg` nos quatro níveis (`c4-nivel1-contexto.jpg`, `c4-nivel2-containers.jpg`, `c4-nivel3-componentes.jpg` e `c4-nivel4-codigo.jpg`), acompanhados de `README.md` com as 5 regras de dependência entre módulos.
* **`docs/contrato-api.md`:** Especificação dos endpoints REST (`/api/v1/...`), cabeçalhos globais (`Authorization` e `X-Polo-Id`), payloads de entrada/saída e códigos de erro HTTP.

---

## 2. Prompt Utilizado para Revisão do Contrato da API

Após redigir a primeira versão de `docs/contrato-api.md`, o arquivo foi submetido à IA juntamente com `docs/historias-priorizadas.md` utilizando o seguinte prompt:

> *"Verifique o seguinte arquivo contrato-api.md descrito abaixo e revise-o contra o historias-priorizadas.md e aponte endpoints faltantes ou inconsistentes."*

---

## 3. Resumo da Resposta da IA (Revisão e Sugestões)

Ao cruzar os fluxos das 5 histórias priorizadas com os endpoints e payloads definidos na primeira versão do contrato, a IA apontou:

1. **Endpoints faltantes para suportar as telas do MVP:**
   * **`GET /api/v1/equipes/`:** Necessário para carregar o seletor de equipes do polo na tela de saída de kits (`HU-016`), já que `POST /api/v1/almoxarifado/saidas-kits/` exige `equipe_id`.
   * **`GET /api/v1/auditoria/`:** Necessário para consultar a trilha imutável de alterações (`RF-PEN-05` / `HU-045`) quando uma OS tem sua prioridade alterada ou é desconsiderada.
   * **`POST /api/v1/auth/logout/`:** Necessário para formalizar o encerramento da sessão autenticada (`HU-019`).
2. **Inconsistências e ambiguidades entre histórias e payloads:**
   * Omissão do campo booleano `pode_visualizar_todos` no retorno de `POST /api/v1/auth/login/`, presente apenas em `GET /api/v1/auth/me/`.
   * Ambiguidade no status HTTP de `POST /api/v1/importacoes/` (`202 Accepted` assíncrono vs. `201 Created` síncrono).
   * Ausência de payload JSON estruturado para o erro `422 Unprocessable Entity` quando a planilha `.xlsx` não possui colunas obrigatórias (`HU-002`).
   * Falta de parâmetros de paginação (`page`, `page_size` e `total`) em `GET /api/v1/ordens-servico/`, embora o critério `CA08` preveja até 5.000 linhas.
   * Indefinição sobre a obrigatoriedade do campo `justificativa` em `PATCH /api/v1/ordens-servico/{id}/prioridade/`.
   * Falta de explicitação sobre a origem do histórico executado no dia anterior (`D-1`) para a trava de kits (`HU-016`), já que a importação de execução (`HU-018`) ficou fora do escopo do protótipo.

---

## 4. O que foi Aceito e o que Não Pôde ser Aceito

### O que foi aceito e incorporado em `docs/contrato-api.md`
* **Novos endpoints de suporte (`GET /api/v1/equipes/`, `GET /api/v1/auditoria/` e `POST /api/v1/auth/logout/`):** Aceitos integralmente para evitar dados fixos (*hardcoded*) no frontend e permitir comprovar a trilha de auditoria na demonstração.
* **Padronização do objeto `usuario` no login:** Aceita a inclusão de `pode_visualizar_todos` em `POST /api/v1/auth/login/` e a definição do tempo de expiração do token (8 horas).
* **Padronização de paginação e erros:** Aceita a inclusão de paginação (`page`, `page_size`, `total`) na listagem de OSs e do JSON detalhado (`CABECALHO_PLANILHA_INVALIDO` com `colunas_faltantes`) no erro `422` da importação.
* **Regras de justificativa e nota de seeds (`D-1`):** Aceita a definição de `justificativa` opcional na priorização (com texto padrão automático) e a documentação explícita de que os dados `D-1` da trava de kits serão populados via *seeds* no banco (Etapa 4).

### O que não pôde ser aceito (e justificativa técnica)
* **Processamento assíncrono real com `202 Accepted`, Celery + Redis e *polling* de progresso:** Não pode ser aceito no contrato do protótipo porque a infraestrutura gratuita exigida na Etapa 2 (Render Free Tier) não oferece *workers* em segundo plano nem servidor Redis gerenciado sem custo. Optou-se por manter a arquitetura modular interna (`ServicoImportacao` e `transaction.atomic()`), mas executando a importação de forma síncrona com retorno `201 Created`.
* **Criação de endpoints para importação da planilha de execução (`HU-018`) para alimentar a trava de kits:** Não pôde ser aceita a inclusão de novos endpoints de execução/auditoria financeira para não extrapolar o limite recomendado de 3 a 5 histórias prioritárias no MVP, mantendo o foco no recorte definido.
* **Endpoint de renovação de token (`POST /api/v1/auth/refresh/`) com rotação em banco:** Não foi aceito por adicionar complexidade de gestão de sessões desnecessária para o protótipo, sendo suficiente o token de turno único (8h) descartado no cliente ao acionar o logout.

---

## 5. Tabela Consolidada de Registro (Modelo da Disciplina)

| Data | Ferramenta (plano) | Etapa | Prompt (resumo) | Resultado e verificação | Ajustes manuais |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 15/11/2026 | Gemini (gratuito) | 1. Pacote de Contexto | Revisar `contrato-api.md` contra `historias-priorizadas.md` apontando endpoints faltantes ou inconsistentes. | Apontou 3 endpoints faltantes (`equipes`, `auditoria`, `logout`) e 6 inconsistências de payload/paginação/status HTTP; sugestões verificadas contra o Projeto Arquitetural e os diagramas C4. | Incorporados os endpoints de consulta, padronizado retorno `201 Created` síncrono para o Render gratuito, adicionada paginação e descartado fluxo assíncrono Celery/Redis e `HU-018` no escopo do MVP. |
| 16/11/2026 | Gemini (gratuito) | 2. Esqueleto ambulante | Gerar configuração inicial do Django + DRF com rota `GET /health` (`SELECT 1;`) conectada ao PostgreSQL Neon e frontend React + TypeScript com Vite | Estrutura criada localmente e validada com retorno `HTTP 200 OK` antes do deploy | Ajustado `DATABASE_URL` no `.env` local e configurado `.gitignore` para bloquear credenciais |
| 16/11/2026 | Gemini (gratuito) | 2. Esqueleto ambulante | Diagnosticar falha de build no Render (`psycopg-binary`) e configurar comunicação CORS entre Vercel e Render | Identificada incompatibilidade do `psycopg-binary==3.2.3` com Python 3.14 no Render e necessidade de liberar origem da Vercel | Atualizado `psycopg[binary]==3.3.9` no `requirements.txt`, fixada versão do Python no Render e atualizado `CORS_ALLOWED_ORIGINS` com a URL da Vercel |
| 20/11/2026 | Claude Code · Opus 5.5 (Pro, pago) | 3. Guia de código | Ler PDF da atividade, ADR, C4 e contrato; rascunhar `AGENTS.md` com camadas, nomes, limites, erros, comentários e testes; configurar ruff, import-linter, ESLint e Prettier | Linters rodando sem erro sobre o esqueleto da Etapa 2; regra de camada testada inserindo `from django.db import ...` numa view (ruff acusou TID251) | Regras **revisadas e aprovadas pelo grupo**; o endpoint `/health` foi refatorado (SQL movido para `nucleo/consultas.py`, `except Exception` trocado por `DatabaseError`, `fetch` movido para `src/servicos/`) |
| 20/11/2026 | Claude Code · Opus 5.5 (Pro, pago) | 4. Banco de dados | Derivar models das 5 histórias + C4 nível 4, com migrations, trigger de auditoria, seeds fictícios, testes de esquema, justificativas e riscos | 23 testes verdes em PostgreSQL 17 local; `migrate` do zero, `migrate zero` e reaplicação OK; seed idempotente (rodado 2×); UPDATE na auditoria recusado pelo trigger | Removido campo `desconsiderada` do C4 (derivado do estado); removido bloqueio de TRUNCATE; PostGIS adiado; ER gerado com Graphviz |
| 21/11/2026 | Claude Code · Opus 5.5 (Pro, pago) | 5. Backend | Implementar, história por história, os endpoints do contrato com services, testes por CA e OpenAPI, seguindo AGENTS.md e o template de prompt | 101 testes verdes em PostgreSQL 17; ruff, lint-imports e makemigrations --check limpos; teste de mutação confirmou que o CA07 (concorrência) falha sem o `select_for_update`; 5.000 linhas importadas em 1,3 s | Agente corrigiu após lint/revisão: views chamando `consultas` direto (passaram a chamar services), helper importado de outra view, polo podendo ficar travado "em andamento" após erro inesperado (`try/finally`); N818 desativado com justificativa. **Revisão humana aprovada** |
| 21/11/2026 | Claude Code · Opus 5.5 (Pro, pago) | 6. Frontend | Uma tela por história consumindo a API só por `src/servicos/`, com estados de carregando/erro/vazio e acessibilidade básica | ESLint/Prettier/build limpos; 9 testes Vitest; roteiro Playwright local passou nos fluxos das 5 histórias, inclusive em 390 px sem rolagem horizontal | `setState` dentro de efeito (regra do react-hooks 7) reescrito; hook com nome fora do padrão; `eslint-disable` trocado por remontagem com `key`; estilo de cabeçalho vazando para `th` de linha. **Revisão humana aprovada** |

## Etapas 3 e 4 — detalhes (Pessoa 2: Deivisson)

### Ferramenta
Claude Code (agente de terminal que lê o repositório) com o modelo Opus 5.5, no plano **Pro (pago)**. O agente lê
`CLAUDE.md` automaticamente, que importa o `AGENTS.md`.

### Prompt inicial (resumo)
> "Chegou a hora de fazer o projeto final (PDF). Eu fiquei como a Pessoa 2 (Etapas 3 e 4). Dê um
> pull e vamos começar."

O agente leu o PDF da atividade, `historias-priorizadas.md`, `contrato-api.md`, ADR-001, o README
dos diagramas C4, a imagem do C4 nível 4 e as histórias HU-004, HU-016, HU-020 e HU-F11 antes de
propor qualquer código.

### Erros e alucinações da IA detectados (insumo para a Etapa 8)

| # | O que a IA fez | Como percebemos | Correção |
|---|---|---|---|
| 1 | Usou na view uma exceção `nucleo.excecoes.BancoIndisponivel` que **não existia** | O ruff passou (não valida imports inexistentes); a própria IA notou ao revisar o diff, antes de rodar | Reescrito: `banco_disponivel()` retorna `bool` e trata `DatabaseError` |
| 2 | Supôs que o import-linter conseguia proibir `django.db` nas views | `lint-imports` falhou: "subpackages of external packages are not valid" | Regra movida para o ruff (`TID251` banned-api só em `views.py`) |
| 3 | Um `sed` para registrar o app `dados_demo` inseriu o nome em **todos** os contratos do `.importlinter` | Contrato de independência quebrou apontando `dados_demo` | Arquivo reescrito à mão |
| 4 | Esperava `InternalError` do trigger; o Django levanta `ProgrammingError` | Testes de imutabilidade falharam | Teste ajustado para o tipo real |
| 5 | Primeiro trigger também bloqueava TRUNCATE | Análise: o `flush` do `TransactionTestCase` usa TRUNCATE, e a Etapa 5 precisa dele para testar a concorrência da trava (HU-016 CA07) | Bloqueio de TRUNCATE removido e risco documentado |

### Divergências da arquitetura (e decisão)
- C4 nível 4 tem `OrdemServico.desconsiderada: bool` → **removido** (duas fontes de verdade); exposto como propriedade.
- ADR prevê PostGIS → **adiado** (seleção por polígono está fora do MVP).
- C4 mostra `Importacao.arquivo: FileField` → **não guardamos o arquivo** (disco efêmero do Render), só nome + hash.
- C4 mostra `Usuario` próprio → **`PerfilUsuario` 1-1 com `auth.User`** (migrations de `auth` já aplicadas no Neon na Etapa 2).

### Proporção aproximada
Estimativa inicial (a conferir pelo grupo após a revisão): gerado pela IA e aceito como veio ~70%; ajustado após revisão/teste ~25%; reescrito à mão ~5%.

---

## Etapas 5 e 6 — detalhes (Pessoa 3: Felipe)

### Ferramenta
Claude Code (agente de terminal que lê o repositório), modelo Opus 5.5. O agente lê `CLAUDE.md`, que
importa o `AGENTS.md`. Plano: **Pro (pago)**.

### Prompt inicial (resumo)
> "Eu fiquei responsável pela Pessoa 3 (Etapas 5 e 6). O Deivisson fez a Pessoa 2 (PDF anexo) e a
> Beatriz a Pessoa 1 (no repositório). Usaremos Vercel, Render e Neon. Analise os artefatos e
> realize as etapas da Pessoa 3. Se tiver dúvida, pergunte. Pode usar contexto do gerOS."

Antes de gerar código, o agente leu o PDF da atividade, o relatório das Etapas 3 e 4, `AGENTS.md`,
contrato, ADR-001, README do C4, `modelo-dados.md`, as histórias HU-001 a HU-008, HU-016, HU-019,
HU-020 e HU-F11, os models, seeds e testes existentes, e o protótipo visual em `docs/design/`.
Do gerOS (sistema real da equipe) aproveitou só a forma de casar cabeçalhos do GSAN sem acento.

Como o pedido foi um só, o agente aplicou internamente o template de `docs/processo/template-prompt.md`
a cada incremento (contexto = história + trecho do contrato; tarefa = um endpoint/tela; critérios =
AGENTS.md §2–§7; restrições = sem dependência não verificada, sem alterar migrations; saída = arquivos +
testes). Cada incremento só foi commitado com lint e testes verdes.

### Erros e alucinações da IA detectados (insumo para a Etapa 8)

| # | O que a IA fez | Como percebemos | Correção |
|---|---|---|---|
| 1 | Deixou um import sem uso (`replace`) e um `__all__` estranho em `nucleo/upsert.py` | Revisão do próprio diff antes de rodar o lint | Removidos |
| 2 | Views chamando `consultas.py` direto (pulando a camada de serviço) | Revisão contra a tabela de camadas do AGENTS.md (o linter não pega: só proíbe `django.db`) | Views passaram a chamar funções de `services.py` |
| 3 | Primeira versão da importação podia deixar o polo travado "em andamento" para sempre se um erro inesperado (não de banco) ocorresse no meio | Análise do fluxo: o índice único parcial bloquearia todos os envios seguintes do polo | `try/finally` marca `FALHOU` e libera o polo |
| 4 | Nomes de exceção em português conflitam com a regra N818 do ruff (exige sufixo `Error`) | `ruff check` | Regra desligada no `pyproject.toml` com justificativa (o AGENTS.md manda `ErroDeNegocio`, `TransicaoNaoPermitida`) |
| 5 | `setState` síncrono dentro de `useEffect` e hook chamado `usarAcoes` | ESLint (`react-hooks/set-state-in-effect`, `rules-of-hooks`) | `useConsulta` reescrito derivando "carregando"; hook renomeado para `useAcoesPendencias` |
| 6 | `eslint-disable` para forçar recarga ao trocar o polo | Revisão: o guia só aceita disable aprovado | Página remontada com `key={polo}` no `App.tsx` |
| 7 | Teste supôs uma ordem fixa na lista de módulos do perfil | Teste falhou | `assertCountEqual` |
| 8 | Captura de tela mostrou importação "VALIDANDO" no histórico | Conferência no banco (estava `CONCLUIDA`) | Não era bug: a captura saiu antes da recarga; roteiro passou a esperar a resposta |

Teste de mutação: removendo o `select_for_update` da trava de kits, o teste do CA07 falhou 3 de 3
vezes; com a trava, passou 3 de 3. Isso mostra que o teste realmente protege a regra.

### Divergências da arquitetura e das histórias
Ver a tabela da seção 4 de `docs/processo/etapas-5-e-6.md` (contrato x HU-001 CA05, sessão de 8 h x
30 min, colunas omitidas, prazo padrão, D-1 corrido, importação síncrona).

### Proporção aproximada
Código gerado pelo agente: ~100% das linhas. Dentro disso, ~80% ficou como saiu na primeira versão e
~20% foi ajustado pelo próprio agente após lint, testes ou revisão contra o AGENTS.md. Reescrito à mão
pelo grupo: 0% até aqui — **a revisão humana (Felipe e grupo) ainda precisa acontecer e atualizar
esta estimativa**.

---

## Incremento 2 — Mapa e roteirização (28/11/2026)

Ferramenta: **Claude Code (Claude Opus, plano Pro pago)**, agente com acesso ao repositório, ao
`AGENTS.md` e ao navegador (Claude in Chrome) para o teste ponta a ponta local. Detalhes do processo em
`docs/processo/incremento-2-roteirizacao.md`.

| Data | Ferramenta (plano) | Etapa | Prompt (resumo) | Resultado e verificação | Ajustes |
|---|---|---|---|---|---|
| 28/11 | Claude Code (Pro) | 1. Contexto | "Analise o backlog, escolha as HUs necessárias para termos o mapa e a roteirização e altere o escopo nas etapas anteriores" | Escolheu HU-024, 060, 011, 012, 031, 056, 013, 014; ADR-002; contrato §7–8 | O board do GitHub Project não pôde ser lido (token sem `read:project`); a escolha usou `docs/historias/` e as issues, que espelham o board |
| 28/11 | Claude Code (Pro) | 4. Banco | Modelar planejamento/rota/item/arquivo e campos de equipe e unidade | 3 migrations; `makemigrations --check` limpo | Ordem dos métodos do model corrigida após `ruff` (DJ012) |
| 28/11 | Claude Code (Pro) | 5. Backend | Uma história por vez, testes citando os CAs | 143 testes verdes (42 novos); `ruff`, `lint-imports` OK | Ver erros 9–12 abaixo |
| 28/11 | Claude Code (Pro) | 6. Frontend | Telas Coordenadas, Roteirizador e liberação em lote, Leaflet | ESLint, Prettier, 17 testes Vitest, build OK | 4 funções divididas por `max-lines-per-function` |
| 28/11 | Claude Code (Pro) | 7. Integração | Percorrer o fluxo no navegador local | Polígono → rota → finalizar → RPA; coordenada fora da área recusada; liberação em lote | Aviso antigo do polígono ficava na tela; download do RPA revogava a URL cedo demais — corrigidos |

### Erros e alucinações detectados neste incremento

| # | O que a IA fez | Como percebemos | Correção |
|---|---|---|---|
| 9 | Seeds herdados com coordenadas de Fortaleza (−3,73; −38,52) para unidades da Paraíba | Teste novo que valida a área de operação (HU-005 RN-L02) falharia | Bairros de João Pessoa com coordenadas aproximadas |
| 10 | Campo extra sem uso (`complementos`) no `PedidoRota` | Revisão do diff | Removido |
| 11 | Teste de matriz de acesso quebrou: o Analista passou a editar o módulo `webscraper` | `python manage.py test` | Expectativa do teste atualizada (mudança intencional da matriz) |
| 12 | Diálogo modal ficaria atrás do mapa (Leaflet usa `z-index` até 1000; o diálogo tinha 10) | Antecipado na revisão do CSS e confirmado no navegador | `z-index: 2000` no fundo do diálogo |
| 13 | Download do RPA via `URL.revokeObjectURL` logo após o clique | Arquivo não apareceu no teste do navegador | Link anexado ao DOM e revogação adiada; **o salvamento no disco não pôde ser confirmado no navegador automatizado** — conferir manualmente |

### Proporção aproximada (Incremento 2)
Código gerado pelo agente: ~100% das linhas novas; ~85% aceito na primeira versão, ~15% ajustado
após linter, testes ou teste no navegador. Reescrito à mão: 0% até a revisão humana do PR.
