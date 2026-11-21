# Etapas 5 e 6 — Backend e Frontend com IA (Pessoa 3: Felipe)

Implementação das 5 histórias do MVP (`docs/historias-priorizadas.md`) sobre o esquema da Etapa 4,
seguindo o `AGENTS.md`, o contrato (`docs/contrato-api.md`) e o ADR-001. Um incremento por história,
cada um com testes e commit próprio (ver `git log`).

## 1. Mapa história → endpoints → tela → testes

| História | Endpoints | Tela | Testes (backend) |
|---|---|---|---|
| HU-019 Login | `POST /auth/login/`, `GET /auth/me/`, `POST /auth/logout/` | Login, cabeçalho com nome/perfil/iniciais, botão Sair | `nucleo/tests/test_autenticacao.py` (CA01–CA03, CA05, CA06, token de 8 h) |
| HU-020 Perfil e polo | cabeçalho `X-Polo-Id` em todas as rotas; `modulos` e `modulos_editaveis` no login | Menu por perfil, seletor global de polo, "Você não tem acesso a esta área" | `nucleo/tests/test_permissoes.py` (CA01, CA03 com `403` para cada célula "—" e cada escrita negada, `TODOS` → 400) |
| HU-F11 Ciclo de vida | usado por `desconsiderar` | — | `nucleo/tests/test_ciclo_de_vida.py` (cada transição permitida, todas as demais recusadas, CA04 varre o código atrás de `.estado =`) |
| HU-001/002/003 Upload, layout, escopo | `POST /importacoes/` | Importação: arrastar/selecionar, validação na tela, resumo e log de alertas | `importacao/tests/test_importacao.py` (HU-001 CA01, CA03–CA08; HU-002 CA02–CA06; HU-003 CA01, CA03, CA04) |
| HU-004 Upsert | `POST /importacoes/`, `GET /importacoes/`, `GET /importacoes/{id}/` | Resumo "Novas / Atualizadas / Ignorados" e histórico | `importacao/tests/test_importacao.py` (CA01–CA07, CA09, RN-L05) |
| HU-006/007/008 Pendências | `GET /ordens-servico/`, `PATCH .../prioridade/`, `POST .../desconsiderar/`, `GET /auditoria/` | Gerenciar Pendências, diálogo de desconsiderar, Trilha de auditoria | `nucleo/tests/test_pendencias.py` (HU-006 CA01, CA04, CA05; HU-008 CA01–CA03; prioridade, desconsiderar, 403/404/409) |
| HU-016 Trava de kit | `GET /equipes/`, `GET /almoxarifado/limites-kits/`, `POST` e `GET /almoxarifado/saidas-kits/` | Almoxarifado: limites do dia, formulário e diálogo "Saída bloqueada" | `almoxarifado/tests/test_saida_kit.py` (CA01–CA08; CA07 com duas threads reais) |

Totais: **101 testes no backend** (PostgreSQL 17) e **9 no frontend** (Vitest). Lint sem erros nos dois lados.

## 2. Como as camadas ficaram

```
views.py        → lê request, valida com serializer, chama service, devolve Response
serializers.py  → formato de entrada/saída (inclui o helper validar)
services.py     → regras, transações, auditoria (CicloDeVidaOS, marcar_prioridade, importar_planilha,
                  registrar_saida_kit...)
consultas.py    → ORM e select_for_update
permissoes.py   → matriz da HU-020 e leitura do X-Polo-Id
excecoes.py     → ErroDeNegocio e filhas, com código e status do contrato
tratamento_erros.py → exception handler único: tudo sai como {"erro": {codigo, mensagem, detalhes}}
```

- O upsert das OSs ficou em `nucleo/upsert.py` (o núcleo é dono da tabela de OS); o módulo de
  importação só lê a planilha (`leitor_planilha.py`), filtra o escopo (`filtro_escopo.py`) e chama o
  serviço do núcleo — regra 3 do AGENTS.md.
- A auditoria do almoxarifado também passa por `nucleo.services.registrar_auditoria`.
- Frontend: só `src/servicos/` chama `fetch` (regra do ESLint). Tipos do contrato em `src/tipos/api.ts`.

## 3. Checklist de revisão (AGENTS.md §11)

| Item | Situação |
|---|---|
| Nomes do domínio em português | ok (`registrar_saida_kit`, `CicloDeVidaOS`, `PaginaPendencias`...) |
| Funções curtas, ≤ 4 parâmetros, linter sem erros | ok (`ruff`, `eslint`); parâmetros agrupados em dataclasses (`PedidoImportacao`, `PedidoSaida`, `Autoria`) |
| Nenhuma regra em `views.py`; ORM só em models/consultas/services | ok (`TID251` + revisão: views chamam só services) |
| Erros específicos no formato do contrato, sem vazar detalhe | ok; teste do CA06 da HU-004 confere que o texto da exceção não chega ao cliente |
| Polo e perfil verificados no servidor | ok (testes de 403 por célula da matriz) |
| Alteração manual grava auditoria na mesma transação | ok (prioridade, desconsideração; tentativa bloqueada de kit) |
| Testes cobrindo os CAs | ok (tabela da seção 1) |
| Contrato e docs atualizados | ok (`docs/contrato-api.md`, README, este arquivo) |
| Alguém do grupo explica cada linha | **pendente: revisão do Felipe e do grupo** |

## 4. Decisões e divergências (para a retrospectiva)

| Ponto | Documento diz | Decisão | Motivo |
|---|---|---|---|
| Tamanho/extensão inválidos | HU-001 CA05: `400` | `413` e `422`, como o contrato | AGENTS.md: "o contrato manda" |
| Expiração da sessão | HU-019 RN-L03: 30 min sem atividade | token de 8 h | contrato §1 (turno operacional) |
| Bloqueio de login | contrato não previa | `429 LOGIN_BLOQUEADO` (HU-019 RN-L02) | contrato atualizado |
| Colunas obrigatórias | HU-002 inclui "Data de Geração" | não exigida | o modelo da Etapa 4 não guarda esse campo |
| Colunas da tela | HU-007 inclui "Data de Geração" e "PP" | omitidas | campo não guardado; "PP" é dúvida aberta na própria história |
| Prazo vazio | HU-008 RN-L02: prazo do tipo (HU-066) | 48 h fixo + alerta | parametrização (HU-066) fora do MVP |
| D-1 | dúvida aberta na HU-016 | dia corrido anterior | o seed cobre todos os dias |
| Processamento assíncrono | ADR-001: Celery + Redis | importação síncrona | Render gratuito não tem worker (decisão da Etapa 1) |
| Planilha com vários polos | dúvida da HU-003 | importação exige polo; unidade de outro polo é descartada | segue RN-L01 da HU-003 |
| Contador de tentativas de login | — | cache em memória do processo | suficiente com 1 worker no Render; com vários workers a contagem fica por worker (risco anotado) |

## 5. Desempenho medido

HU-004 CA08 (5.000 linhas em até 3 min): **1,3 s** na primeira carga e **3,5 s** na reimportação, em
PostgreSQL local. No Neon a latência de rede aumenta o tempo, mas o upsert faz uma única consulta das
OSs existentes e grava em lotes de 500 (`bulk_create`/`bulk_update`).

## 6. Publicação (o que muda no Render e na Vercel)

- **Render:** depende de `python manage.py migrate` no deploy — esta etapa acrescenta a tabela de
  tokens (`authtoken`) e precisa das migrations da Etapa 4. Conferir se o *Build/Start Command* do
  serviço roda `migrate` (por exemplo, `pip install -r requirements.txt && python manage.py migrate`).
  Dependências novas em `requirements.txt`: `openpyxl` (leitura do `.xlsx`) e `drf-spectacular` (OpenAPI).
  Nenhuma variável de ambiente nova.
- **Neon:** rodar `popular_dados_demo` com `SENHA_USUARIOS_DEMO` para criar os usuários da demonstração.
- **Vercel:** `VITE_API_URL` já existe. O `frontend/vercel.json` faz as rotas da SPA (`/pendencias`,
  `/importacao`...) abrirem direto pela URL.

## 7. Pendências

- Revisão humana do código e das decisões da seção 4 pelo grupo.
- Deploy no Render/Neon (acesso ao projeto Neon ainda não liberado para a Pessoa 3).
- Etapa 7 (Pessoa 4): testes ponta a ponta nas URLs publicadas. Um roteiro com Playwright foi usado
  localmente nesta etapa (login → pendências → importação → almoxarifado → auditoria, também em 390 px
  de largura) e pode servir de base.
