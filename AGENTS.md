# Guia de código do GeniOS (regras para humanos e IA)

Este arquivo é lido automaticamente por agentes de código (Claude Code, Cursor, Copilot, Codex).
Em ferramentas de chat que não leem o repositório, **cole este arquivo no início de cada conversa**.
Toda regra aqui é verificável: ou por linter (`ruff`, `lint-imports`, `eslint`), ou por testes, ou por
revisão com o checklist do final.

## 1. Contexto obrigatório

Antes de gerar código, leia:

| Documento | Para quê |
|---|---|
| `docs/historias-priorizadas.md` | Escopo do MVP (5 histórias) e do Incremento 2 (roteirização, 8 histórias) |
| `docs/contrato-api.md` | Endpoints, payloads e erros — **o contrato manda** |
| `docs/adr/ADR-001-arquitetura-mvp.md` | Monólito modular, stack |
| `docs/adr/ADR-002-mapa-e-roteirizacao.md` | Leaflet/OSM, polígono no navegador, layout RPA |
| `docs/diagramas-c4/README.md` | Regras de dependência entre módulos |
| `docs/banco/modelo-dados.md` | Tabelas, restrições e o que cada história lê/grava |
| `docs/historias/HU-xxx-*.md` | Critérios de aceite completos de cada história |

Se o pedido contradiz um desses documentos, **pare e aponte a contradição** em vez de escolher sozinho.

## 2. Arquitetura em camadas

### Backend (Django + DRF) — um app por módulo de negócio

```
backend/
  config/          configuração do Django (settings, urls raiz)
  nucleo/          compartilhado: Polo, Unidade, Equipe, Perfil, OrdemServico, Auditoria
  importacao/      HU-001..004: planilha GSAN e upsert
  almoxarifado/    HU-016: tipos de kit, execução D-1, saídas
  roteirizacao/    HU-011..014, HU-056: operações, planejamento, rotas, arquivo RPA
```

Dentro de cada app:

| Camada | Arquivo | Pode | Não pode |
|---|---|---|---|
| Rota | `views.py` | ler request, chamar serializer e service, devolver Response | regra de negócio, `Model.objects`, SQL, `transaction` |
| Validação de entrada/saída | `serializers.py` | validar formato e tipos, formatar resposta | regra de negócio, gravar no banco |
| Regra de negócio | `services.py` (ou `services_<assunto>.py` quando passaria de 300 linhas) | regras, transações (`transaction.atomic`), chamar consultas e auditoria | conhecer `request`/`Response`/HTTP |
| Acesso a dados | `models.py`, `consultas.py` | ORM, `select_for_update`, agregações | regra de negócio |
| Permissões | `permissoes.py` | checar perfil e polo | regra de negócio |

Regras de dependência (verificadas por `lint-imports`, ver `backend/.importlinter`):

1. `views.py` não importa `django.db` (nada de ORM ou transação na rota).
2. `nucleo` não importa nenhum módulo de negócio (`importacao`, `almoxarifado`, `roteirizacao`).
3. Módulos de negócio não importam um ao outro; um módulo não grava nas tabelas de outro — chama o
   `services.py` do módulo dono.
4. O estado da OS só muda por `nucleo.services.CicloDeVidaOS.transicionar` (HU-F11). Nunca
   `os.estado = ...` fora dele. Outros módulos pedem a transição a `nucleo.services_preparacao`.
5. Toda alteração manual de dado operacional grava `RegistroAuditoria` **na mesma transação**.
   A tabela é append-only (trigger no PostgreSQL bloqueia UPDATE/DELETE).
6. Toda consulta filtra por polo (`X-Polo-Id`) no servidor. Escrita exige polo específico (`TODOS` → 400).

### Frontend (React + TypeScript + Vite)

```
frontend/src/
  servicos/       únicos arquivos que chamam fetch (cliente HTTP, headers Authorization e X-Polo-Id)
  tipos/          tipos TypeScript espelhando o contrato da API
  hooks/          estado e efeitos reutilizáveis (useOrdensServico, usePoloSelecionado...)
  componentes/    componentes de UI sem chamada direta à API
  paginas/        uma pasta por tela, compõe hooks e componentes
```

- Só `servicos/` chama `fetch`. Componentes e páginas nunca montam URL nem headers.
- URL da API vem de `import.meta.env.VITE_API_URL`; nenhum endereço fixo no código.
- Toda tela que consome API trata **carregando, erro e lista vazia** (o Render hiberna ~1 min).
- Acessibilidade: todo campo tem `<label>`, tudo operável por teclado, contraste AA.

## 3. Convenções de nomes

- **Idioma do domínio em português**, sem acento em identificadores: `OrdemServico`, `prazo_horas`,
  `registrar_saida_kit`. Termos técnicos do framework ficam em inglês (`serializer`, `queryset`).
- Python: `snake_case` para funções/variáveis, `PascalCase` para classes, `MAIUSCULAS` para constantes.
- TypeScript: `camelCase` para funções/variáveis, `PascalCase` para componentes e tipos; um
  componente por arquivo com o mesmo nome (`TabelaOrdensServico.tsx`).
- Nomes revelam intenção: `calcular_atraso_horas`, não `calc` ou `processa_dados`. Booleanos com
  `e_`/`pode_`/`tem_` ou adjetivo (`em_atraso`, `pode_visualizar_todos`).
- Códigos de erro de negócio em `MAIUSCULAS_COM_UNDERSCORE` (`TRAVA_HISTORICO_KIT_EXCEDIDA`).

## 4. Limites de tamanho (verificados pelo linter)

| Limite | Backend (ruff) | Frontend (eslint) |
|---|---|---|
| Parâmetros por função | 4 (`PLR0913`) | 4 (`max-params`) |
| Complexidade ciclomática | 8 (`C901`) | 8 (`complexity`) |
| Comandos por função | 30 (`PLR0915`) | 60 linhas por função (`max-lines-per-function`) |
| Ramificações por função | 8 (`PLR0912`) | aninhamento máx. 3 (`max-depth`) |
| Retornos por função | 4 (`PLR0911`) | — |
| Linhas por arquivo | revisão: 300 | 300 (`max-lines`) |

Se um limite estoura, **divida a função** — não desligue a regra. `# noqa` / `eslint-disable` só com
comentário explicando o porquê, e precisa ser aprovado na revisão.

## 5. Tratamento de erros

- Erros de negócio são exceções específicas herdando de `nucleo.excecoes.ErroDeNegocio`, com
  `codigo`, `mensagem` e `detalhes`. Ex.: `TransicaoNaoPermitida`, `TravaHistoricoExcedida`.
- Um único exception handler do DRF converte essas exceções no formato do contrato:
  `{"erro": {"codigo", "mensagem", "detalhes"}}` com o status HTTP definido na exceção.
- **Proibido** `except Exception` / `except:` genérico (`BLE001`, `E722`). Capture a exceção específica
  (`DatabaseError`, `InvalidFileException`...).
- Nunca devolver `str(exc)` ou stack trace ao cliente; logue no servidor e devolva mensagem clara.
- No frontend, `servicos/` converte respostas de erro em `ErroApi` tipado; a tela mostra `mensagem`.

## 6. Comentários e documentação

- O código explica **o quê**; comentário explica **por quê** (regra de negócio, decisão, armadilha).
  Cite a regra: `# RN-11: trava de histórico compara a soma do dia`.
- Docstring curta em toda função pública de `services.py`.
- Proibido código comentado (`ERA001`) e comentário que repete o código.
- Endpoint novo ou alterado → atualizar `docs/contrato-api.md` no mesmo commit.

## 7. Testes

- Todo service e toda regra de negócio têm teste. Escreva o teste **antes** da implementação.
- Cada critério de aceite (CA) de história no escopo vira pelo menos um teste; o nome cita o CA:
  `test_ca03_os_desconsiderada_continua_desconsiderada`.
- Testes rodam contra **PostgreSQL** (constraints e triggers são do Postgres): `python manage.py test`.
- Dados de teste são fictícios. Nunca dados pessoais reais.

## 8. Segurança e dados (LGPD)

- Segredos só em variáveis de ambiente (`.env`, nunca versionado). Nunca cole segredos em prompts.
- Guarde apenas o dado pessoal estritamente necessário (nome e e-mail do usuário do sistema).
- Autorização sempre no servidor: perfil (HU-020) **e** polo (`X-Polo-Id`).
- Dependência nova só depois de confirmar que existe, é mantida e é necessária; fixe a versão.

## 9. Fluxo de trabalho

- Uma história por vez; um incremento que funciona = um commit.
- Mensagens no padrão `tipo: descrição` em português (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`).
- Antes de commitar:
  - backend: `ruff format --check . && ruff check . && lint-imports && python manage.py test`
  - frontend: `npm run format:check && npm run lint && npm run build`
- Registre cada interação relevante com IA em `docs/registro-uso-ia.md`.

## 10. Estrutura fixa de prompt

Use o modelo em `docs/processo/template-prompt.md`: **contexto, tarefa, critérios de qualidade,
restrições e formato de saída**.

## 11. Checklist de revisão do código gerado

- [x] Nomes do domínio, em português, revelando intenção
- [x] Funções curtas, até 4 parâmetros, linter sem erros
- [x] Nenhuma regra de negócio em `views.py`; nenhum ORM/SQL fora de `models.py`/`consultas.py`/`services.py`
- [x] Erros específicos, no formato do contrato, sem vazar detalhes internos
- [x] Polo e perfil verificados no servidor
- [x] Alteração manual grava auditoria na mesma transação
- [x] Testes cobrindo os CAs, rodando verde
- [x] Contrato da API e docs atualizados
- [x] Alguém do grupo consegue explicar cada linha
