# Contrato da API REST — GeniOS (Escopo MVP)

Este documento define os endpoints, cabeçalhos globais, estruturas de entrada, respostas de sucesso e códigos de erro da API do **GeniOS** (Django + Django REST Framework), alinhados às 5 histórias de usuário priorizadas em `docs/historias-priorizadas.md` e aos diagramas C4 em `docs/diagramas-c4/`.

---

## 1. Convenções Gerais

* **Base URL:** `/api/v1`
* **Formato de dados:** `application/json` (exceto upload de planilhas, que utiliza `multipart/form-data`).
* **Autenticação e Sessão (`HU-019`):**
  * Header obrigatório: `Authorization: Bearer <access_token>` em todas as rotas, exceto `POST /api/v1/auth/login/` e `GET /health/`.
  * Tempo de expiração do token no MVP: **8 horas** (um turno operacional). Ao encerrar a sessão em `POST /api/v1/auth/logout/`, o cliente descarta o token armazenado.
* **Filtro Global de Polo (`HU-020` / `RF-TRV-02`):**
  * Todas as requisições autenticadas devem enviar o cabeçalho **`X-Polo-Id`** contendo o ID numérico do polo selecionado (`1`, `2`, `3`) ou o valor literal `TODOS`.
  * **Leitura (`GET`):** Aceita `X-Polo-Id: TODOS` (retorna registros de todos os polos permitidos ao usuário) ou um ID específico.
  * **Escrita (`POST`, `PATCH`, `PUT`, `DELETE`):** Exige um polo específico (`1`, `2` ou `3`). Caso `X-Polo-Id` seja `TODOS` ou ausente, o servidor bloqueia a operação com **`400 Bad Request`**.
  * **Autorização de Polo:** Se o usuário tentar consultar ou alterar um polo ao qual não possui vínculo, o servidor retorna **`403 Forbidden`**.

### Padrão de Resposta de Erro
```json
{
  "erro": {
    "codigo": "CODIGO_DE_NEGOCIO_OU_VALIDACAO",
    "mensagem": "Descrição clara do erro para exibição ao usuário.",
    "detalhes": {}
  }
}
```

---

## 2. Saúde da Infraestrutura (Esqueleto Ambulante)

### `GET /health/`
Verifica a disponibilidade da API e a conectividade com o banco de dados PostgreSQL (`SELECT 1`).

* **Autenticação:** Pública.
* **Entrada:** Nenhuma.
* **Saída (`200 OK`):**
```json
{
  "status": "ok",
  "api": "API OK",
  "banco": "Banco OK"
}
```
* **Erros:**
  * `503 Service Unavailable`: Falha de conexão com o banco de dados (`"banco": "Banco Indisponível"`).

---

## 3. Autenticação e Controle de Polo (`HU-019` e `HU-020`)

### `POST /api/v1/auth/login/`
Autentica um usuário individual e retorna seu token de acesso, perfil, permissão de visão global e lista de polos autorizados.

* **Entrada (`application/json`):**
```json
{
  "email": "ana.analista@genios.com.br",
  "senha": "********"
}
```
* **Saída (`200 OK`):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "usuario": {
    "id": 12,
    "nome": "Ana Beatriz",
    "email": "ana.analista@genios.com.br",
    "perfil": "ANALISTA_OPERACOES",
    "pode_visualizar_todos": true,
    "polos_autorizados": [
      { "id": 1, "codigo": "POLO_1", "nome": "Polo 1 - Central" },
      { "id": 2, "codigo": "POLO_2", "nome": "Polo 2 - Norte" },
      { "id": 3, "codigo": "POLO_3", "nome": "Polo 3 - Sul" }
    ]
  }
}
```
* **Erros:**
  * `400 Bad Request`: Campos `email` ou `senha` ausentes.
  * `401 Unauthorized`: Credenciais inválidas ou usuário inativo. Mensagem única `"E-mail ou senha inválidos"`, sem revelar se o e-mail existe (`HU-019 RN-L05`).
  * `429 Too Many Requests` (`LOGIN_BLOQUEADO`): 5 tentativas erradas seguidas bloqueiam o e-mail por 15 minutos (`HU-019 RN-L02`). *Acrescentado na Etapa 5.*
* **Campo `usuario.modulos` (acrescentado na Etapa 5):** lista dos módulos que o perfil pode abrir (`importacao`, `pendencias`, `equipes`, `almoxarifado`, `auditoria`), derivada da matriz da `HU-020`. O frontend monta o menu com ela; o servidor continua checando cada rota. `usuario.modulos_editaveis` lista os módulos em que o perfil pode gravar (a tela esconde as ações dos demais).

---

### `GET /api/v1/auth/me/`
Retorna os dados do usuário autenticado e seus polos permitidos para manter o estado do cabeçalho na aplicação web.

* **Cabeçalhos:** `Authorization: Bearer <token>`
* **Entrada:** Nenhuma.
* **Saída (`200 OK`):** mesmo objeto `usuario` do login, incluindo `modulos`.
```json
{
  "id": 12,
  "nome": "Ana Beatriz",
  "email": "ana.analista@genios.com.br",
  "perfil": "ANALISTA_OPERACOES",
  "pode_visualizar_todos": true,
  "polos_autorizados": [
    { "id": 1, "codigo": "POLO_1", "nome": "Polo 1 - Central" },
    { "id": 2, "codigo": "POLO_2", "nome": "Polo 2 - Norte" },
    { "id": 3, "codigo": "POLO_3", "nome": "Polo 3 - Sul" }
  ]
}
```
* **Erros:**
  * `401 Unauthorized`: Token ausente (`NAO_AUTENTICADO`), inválido ou com mais de 8 horas (`SESSAO_INVALIDA`).

---

### `POST /api/v1/auth/logout/`
Encerra a sessão ativa do usuário autenticado.

* **Cabeçalhos:** `Authorization: Bearer <token>`
* **Entrada:** Nenhuma.
* **Saída (`204 No Content`):** Sem corpo de resposta. O token é apagado no servidor: reutilizá-lo devolve `401` (`HU-019 CA05`).
* **Erros:**
  * `401 Unauthorized`: Token ausente ou inválido.

---

## 4. Importação Transacional da Planilha GSAN (`HU-001`, `HU-002`, `HU-003`, `HU-004`)

### `POST /api/v1/importacoes/`
Recebe a planilha `.xlsx` do GSAN, valida extensão, tamanho e cabeçalho obrigatório, filtra unidades fora do escopo contratual e executa o upsert transacional sem amnésia (`CA01` a `CA09`) de forma síncrona no MVP.

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int>` (não aceita `TODOS`)
* **Entrada (`multipart/form-data`):**
  * `arquivo` (obrigatório): Arquivo `.xlsx` de até 25 MB.
* **Saída (`201 Created`):**
```json
{
  "id": 48,
  "polo_id": 1,
  "status": "CONCLUIDA",
  "etapa": "FINALIZADA",
  "percentual": 100,
  "hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "resumo": {
    "total_linhas": 150,
    "novas": 42,
    "atualizadas": 98,
    "fora_escopo": 10
  },
  "alertas": [
    {
      "linha": 87,
      "campo": "prazo_horas",
      "motivo": "Prazo preenchido com valor padrão do contrato."
    }
  ],
  "iniciada_em": "2026-11-16T08:10:00-03:00",
  "concluida_em": "2026-11-16T08:10:04-03:00"
}
```
* **Erros:**
  * `400 Bad Request`: `X-Polo-Id` igual a `TODOS` ou arquivo não enviado.
  * `403 Forbidden`: Perfil sem permissão de importação (`PodeImportar`) ou sem acesso ao polo.
  * `400 Bad Request` (`MAIS_DE_UM_ARQUIVO`): mais de um arquivo no campo `arquivo` (`HU-001 CA08`).
  * `409 Conflict`: Já existe uma importação em andamento para o mesmo polo (`garantir_unica_em_andamento`).
  * `413 Payload Too Large` (`ARQUIVO_MUITO_GRANDE`): Arquivo excede 25 MiB (26.214.400 bytes). Nada é registrado.
  * `422 Unprocessable Entity` (`FORMATO_NAO_ACEITO`): extensão diferente de `.xlsx`. Nada é registrado.
  * `422 Unprocessable Entity` (`PLANILHA_ILEGIVEL`): o `.xlsx` não abre (arquivo truncado). A importação fica `RECUSADA`.
  * `500 Internal Server Error` (`IMPORTACAO_FALHOU`): falha de banco durante o upsert; nada foi gravado (tudo ou nada) e a importação fica `FALHOU`, liberando o polo para novo envio.
* **Layout da planilha (`HU-002`):** primeira aba; cabeçalho na linha 1; colunas obrigatórias `Ordem de Serviço`, `Especificação`, `Tipo`, `Nº do Imóvel`, `Unidade Atual`, `Cidade`, `Setor`, `Quadra`, `Prazo (h)` e `Abertura` (comparadas sem acento e sem caixa; ordem livre; colunas extras ignoradas). `Unidade Atual` pode trazer o código ou o nome da unidade. Linha inválida não interrompe a importação: vira item de `alertas`. Prazo vazio usa 48 h com alerta.
  * `422 Unprocessable Entity` (Colunas obrigatórias ausentes — arquivo recusado integralmente sem gravar OSs; a importação fica `RECUSADA` com o motivo):
```json
{
  "erro": {
    "codigo": "CABECALHO_PLANILHA_INVALIDO",
    "mensagem": "Colunas obrigatórias ausentes: Setor, Quadra",
    "detalhes": {
      "colunas_faltantes": ["Setor", "Quadra"]
    }
  }
}
```

---

### `GET /api/v1/importacoes/{id}/`
Consulta o status (`RECEBIDA`, `VALIDANDO`, `FILTRANDO`, `GRAVANDO`, `CONCLUIDA`, `RECUSADA`, `FALHOU`) e o resumo consolidado de uma importação específica.

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int | TODOS>`
* **Entrada (Path):** `id` (inteiro, ID da importação).
* **Saída (`200 OK`):** Mesmo objeto JSON retornado em `POST /api/v1/importacoes/`, acrescido de `motivo_falha` (string ou `null`).
* **Erros:**
  * `403 Forbidden`: Importação pertence a um polo não autorizado ao usuário.
  * `404 Not Found`: Importação não encontrada.

---

### `GET /api/v1/importacoes/`
Lista o histórico de importações realizadas no(s) polo(s) selecionado(s).

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int | TODOS>`
* **Entrada (Query opcional):** `?status=CONCLUIDA&page=1&page_size=20`
* **Saída (`200 OK`):**
```json
{
  "total": 2,
  "resultados": [
    {
      "id": 48,
      "polo": "Polo 1 - Central",
      "usuario": "Ana Beatriz",
      "status": "CONCLUIDA",
      "hash_sha256": "e3b0c442...",
      "total_linhas": 150,
      "novas": 42,
      "atualizadas": 98,
      "fora_escopo": 10,
      "iniciada_em": "2026-11-16T08:10:00-03:00"
    }
  ]
}
```
* **Erros:**
  * `401 Unauthorized`: Não autenticado.
  * `403 Forbidden`: Polo não autorizado.

---

## 5. Listagem, Tratamento de Pendências e Auditoria de OS (`HU-006`, `HU-007`, `HU-008`)

### `GET /api/v1/ordens-servico/`
Lista as Ordens de Serviço filtradas pelo polo do cabeçalho, retornando contadores por estado, paginação e os cálculos de tempo decorrido e atraso (`RN-06`).

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int | TODOS>`
* **Entrada (Query opcional):**
  * `estado`: `PENDENTE`, `APTA_A_ROTEIRIZAR`, `DESCONSIDERADA`, etc. (padrão: `PENDENTE`)
  * `prioridade`: `true` ou `false`
  * `atrasada`: `true` ou `false`
  * `busca`: filtro por número da OS, setor ou unidade
  * `page`: número da página (padrão: `1`)
  * `page_size`: itens por página (padrão: `50`, máximo: `200`)
* **Saída (`200 OK`):**
```json
{
  "total": 120,
  "contadores_por_status": {
    "PENDENTE": 120,
    "APTA_A_ROTEIRIZAR": 18,
    "DESCONSIDERADA": 5
  },
  "resultados": [
    {
      "id": 901,
      "numero": "20260004512",
      "polo": { "id": 1, "nome": "Polo 1 - Central" },
      "unidade": { "codigo": "UN-04", "nome": "ETA Central", "latitude": "-3.731900", "longitude": "-38.526700" },
      "tipo": "RELIGACAO_AGUA",
      "especificacao": "Religação no cavalete",
      "numero_imovel": "1234",
      "cidade": "Cidade Demo",
      "setor": "012",
      "quadra": "045",
      "estado": "PENDENTE",
      "prioridade": true,
      "desconsiderada": false,
      "equipe_id": null,
      "abertura": "2026-11-15T10:00:00-03:00",
      "prazo_horas": 24,
      "tempo_decorrido_horas": 26.5,
      "atraso_horas": 2.5,
      "em_atraso": true
    }
  ]
}
```
* **Notas (Etapa 5):** `numero_imovel`, `cidade` e as coordenadas da unidade foram acrescentados para as colunas da `HU-007`. `atraso_horas` negativo indica quanto falta para vencer (faixa "vence em até 4 h" da `HU-008 RN-L03`); `em_atraso` só é `true` quando o atraso passa de zero. Ordenação: prioritárias primeiro, depois maior atraso (`HU-006 RN-L02`). `contadores_por_status` considera os polos selecionados, sem os demais filtros.
* **Erros:**
  * `400 Bad Request`: Parâmetro de filtro ou paginação inválido.
  * `403 Forbidden`: Polo não autorizado.

---

### `PATCH /api/v1/ordens-servico/{id}/prioridade/`
Marca ou desmarca uma OS como prioritária (tratamento manual preservado em reimportações futuras, conforme `CA02`) e grava registro na `TrilhaAuditoria`.

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int>` (não aceita `TODOS`)
* **Entrada (Path + JSON):**
  * Path: `id` (inteiro, ID da OS)
  * Body (`justificativa` é opcional; quando omitida, o sistema registra `"Alteração manual de prioridade"`):
```json
{
  "prioridade": true,
  "justificativa": "Solicitação emergencial de unidade hospitalar."
}
```
* **Saída (`200 OK`):**
```json
{
  "id": 901,
  "numero": "20260004512",
  "prioridade": true,
  "estado": "PENDENTE",
  "atualizado_por": "Ana Beatriz"
}
```
* **Erros:**
  * `400 Bad Request`: `X-Polo-Id` igual a `TODOS` ou campo `prioridade` ausente.
  * `403 Forbidden`: Usuário sem permissão ou OS de outro polo.
  * `404 Not Found`: Ordem de serviço não encontrada.
  * `409 Conflict`: OS encontra-se em estado terminal (`DESCONSIDERADA` ou `FATURADA`) que não permite alteração.

---

### `POST /api/v1/ordens-servico/{id}/desconsiderar/`
Transiciona a OS para o estado terminal `DESCONSIDERADA` por meio da máquina de estados `CicloDeVidaOS` (`CA03`, `HU-F11`), registra justificativa obrigatória na `TrilhaAuditoria` e garante que reimportações futuras não reativem a OS.

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int>` (não aceita `TODOS`)
* **Entrada (Path + JSON):**
  * Path: `id` (inteiro, ID da OS)
  * Body (`justificativa` obrigatória):
```json
{
  "justificativa": "OS aberta em duplicidade no GSAN para o mesmo imóvel."
}
```
* **Saída (`200 OK`):**
```json
{
  "id": 901,
  "numero": "20260004512",
  "estado": "DESCONSIDERADA",
  "desconsiderada": true,
  "auditoria_registrada": true
}
```
* **Erros:**
  * `400 Bad Request`: `justificativa` vazia/ausente ou `X-Polo-Id` igual a `TODOS`.
  * `403 Forbidden`: Usuário sem permissão ou OS de outro polo.
  * `404 Not Found`: Ordem de serviço não encontrada.
  * `409 Conflict`: Transição inválida segundo `CicloDeVidaOS.TRANSICOES` (ex.: OS já está `EXECUTADA` ou `FATURADA`).

---

### `GET /api/v1/auditoria/`
Consulta os registros imutáveis da trilha de auditoria (`RF-PEN-05`, `HU-045`) para comprovar alterações manuais de prioridade e desconsideração de OSs.

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int | TODOS>`
* **Entrada (Query opcional):** `?entidade=OrdemServico&entidade_id=901`
* **Saída (`200 OK`):**
```json
{
  "resultados": [
    {
      "id": 15,
      "entidade": "OrdemServico",
      "entidade_id": 901,
      "campo": "estado",
      "valor_anterior": "PENDENTE",
      "valor_novo": "DESCONSIDERADA",
      "justificativa": "OS aberta em duplicidade no GSAN para o mesmo imóvel.",
      "autor": "Ana Beatriz",
      "origem": "TELA",
      "registrado_em": "2026-11-16T09:15:00-03:00"
    }
  ]
}
```
* **Erros:**
  * `401 Unauthorized`: Não autenticado.
  * `403 Forbidden`: Polo não autorizado.

---

## 6. Bloqueio de Saída de Kit por Trava de Histórico (`HU-016`)

> **Nota de Escopo MVP:** Como a importação da planilha de execução (`HU-018`) está fora das 5 histórias priorizadas, os registros de volume executado no dia anterior (`D-1`) utilizados pela trava de histórico são carregados via **seeds iniciais do banco de dados (Etapa 4)**.

### `GET /api/v1/equipes/`
Lista as equipes ativas vinculadas ao(s) polo(s) selecionado(s) para preenchimento do formulário de saída de kits.

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int | TODOS>`
* **Entrada (Query opcional):** `?ativa=true`
* **Saída (`200 OK`):**
```json
{
  "resultados": [
    {
      "id": 7,
      "codigo": "EQ-07",
      "nome": "João / Marcos",
      "polo_id": 1,
      "ativa": true
    }
  ]
}
```
* **Erros:**
  * `401 Unauthorized`: Não autenticado.
  * `403 Forbidden`: Polo não autorizado.

---

### `GET /api/v1/almoxarifado/limites-kits/`
Consulta o teto diário permitido para retirada de cada tipo de kit no polo selecionado, calculado a partir do volume executado no dia anterior (`D-1`).

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int>` (não aceita `TODOS`)
* **Entrada (Query opcional):** `?data=2026-11-16` (padrão: data atual do servidor)
* **Saída (`200 OK`):**
```json
{
  "polo_id": 1,
  "data_referencia": "2026-11-16",
  "kits": [
    {
      "kit_id": 3,
      "tipo_kit": "KIT_LIGACAO_NOVA_1_2",
      "nome": "Kit Ligação Nova 1/2",
      "executado_dia_anterior": 25,
      "saidas_registradas_hoje": 15,
      "saldo_disponivel_hoje": 10
    }
  ]
}
```
* **Erros:**
  * `400 Bad Request`: `X-Polo-Id` igual a `TODOS`.
  * `403 Forbidden`: Polo não autorizado.

---

### `POST /api/v1/almoxarifado/saidas-kits/`
Registra a saída de kits para uma equipe de campo, aplicando no servidor a trava de histórico (`RN-11`: bloqueia se `saidas_hoje + quantidade > executado_ontem`).

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int>` (não aceita `TODOS`)
* **Entrada (`application/json`):**
```json
{
  "equipe_id": 7,
  "kit_id": 3,
  "quantidade": 12
}
```
* **Saída (`201 Created`):**
```json
{
  "id": 304,
  "polo_id": 1,
  "equipe_id": 7,
  "tipo_kit": "KIT_LIGACAO_NOVA_1_2",
  "quantidade": 12,
  "data_saida": "2026-11-16T07:30:00-03:00",
  "registrado_por": "Carlos Almoxarife"
}
```
* **Erros:**
  * `400 Bad Request`: Quantidade menor ou igual a zero, campos obrigatórios ausentes ou `X-Polo-Id` igual a `TODOS`.
  * `403 Forbidden`: Perfil sem permissão de almoxarifado ou equipe de outro polo.
  * `404 Not Found`: Equipe ou tipo de kit não encontrado.
  * `422 Unprocessable Entity` (Trava de Histórico acionada):
```json
{
  "erro": {
    "codigo": "TRAVA_HISTORICO_KIT_EXCEDIDA",
    "mensagem": "Saída bloqueada: Kit Ligação Nova 1/2 · Solicitado hoje: 27 un. · Executado ontem: 25 un.",
    "detalhes": {
      "tipo_kit": "KIT_LIGACAO_NOVA_1_2",
      "quantidade_solicitada": 12,
      "ja_retirado_hoje": 15,
      "limite_executado_ontem": 25
    }
  }
}
```

---

### `GET /api/v1/almoxarifado/saidas-kits/`
Lista as saídas de kits registradas no(s) polo(s) selecionado(s).

* **Cabeçalhos:** `Authorization: Bearer <token>`, `X-Polo-Id: <int | TODOS>`
* **Entrada (Query opcional):** `?data=2026-11-16`
* **Saída (`200 OK`):**
```json
{
  "resultados": [
    {
      "id": 304,
      "polo": "Polo 1 - Central",
      "equipe": "EQ-07 (João / Marcos)",
      "tipo_kit": "KIT_LIGACAO_NOVA_1_2",
      "quantidade": 12,
      "data_saida": "2026-11-16T07:30:00-03:00",
      "registrado_por": "Carlos Almoxarife"
    }
  ]
}
```
* **Erros:**
  * `401 Unauthorized`: Não autenticado.
  * `403 Forbidden`: Polo não autorizado.

---

* **Regras implementadas (Etapa 5):** a soma do dia inclui a saída pedida (`RN-L01`); D-1 é o dia corrido anterior; sem execução em D-1 o limite é 0 (`RN-L02`); a linha de execução D-1 é travada com `SELECT ... FOR UPDATE` para que duas saídas simultâneas não passem do limite (`CA07`); a tentativa bloqueada é gravada na trilha de auditoria (`entidade = "SaidaKit"`, `campo = "tentativa_bloqueada"`, `CA08`). A equipe precisa ser do polo do cabeçalho (`403`) e estar ativa (`400`).

---

## 7. Documentação interativa (OpenAPI)

O esquema OpenAPI é gerado a partir do código com `drf-spectacular`:
* `GET /api/schema/` — esquema OpenAPI 3 (YAML).
* `GET /api/docs/` — Swagger UI para explorar e testar os endpoints (use o botão *Authorize* com `Bearer <token>`).

Este documento continua sendo o contrato de referência; o esquema gerado serve para conferir que o código o implementa.

---

## 8. Matriz de Rastreabilidade (Histórias x Endpoints)

| História Priorizada | Requisitos | Endpoints Correspondentes |
| :--- | :--- | :--- |
| **1. Acesso e Filtro Global por Polo (`HU-019`, `HU-020`)** | `RF-TRV-01` a `03` | `POST /api/v1/auth/login/`, `GET /api/v1/auth/me/`, `POST /api/v1/auth/logout/` + cabeçalho `X-Polo-Id` |
| **2. Upload, Validação e Escopo GSAN (`HU-001` a `HU-003`)** | `RF-IMP-01` a `03` | `POST /api/v1/importacoes/` |
| **3. Importação Transacional Sem Amnésia (`HU-004`)** | `RF-IMP-04`, `05`, `CA01-09` | `POST /api/v1/importacoes/`, `GET /api/v1/importacoes/{id}/`, `GET /api/v1/importacoes/` |
| **4. Listagem e Tratamento de Pendências (`HU-006` a `HU-008`)** | `RF-PEN-01` a `05` | `GET /api/v1/ordens-servico/`, `PATCH /api/v1/ordens-servico/{id}/prioridade/`, `POST /api/v1/ordens-servico/{id}/desconsiderar/`, `GET /api/v1/auditoria/` |
| **5. Bloqueio de Saída de Kit (`HU-016`)** | `RF-ALM-01`, `03`, `04` | `GET /api/v1/equipes/`, `GET /api/v1/almoxarifado/limites-kits/`, `POST /api/v1/almoxarifado/saidas-kits/`, `GET /api/v1/almoxarifado/saidas-kits/` |