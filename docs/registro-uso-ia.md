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
* **Processamento assíncrono real com `202 Accepted`, Celery + Redis e *polling* de progresso:** Não pôde ser aceito no contrato do protótipo porque a infraestrutura gratuita exigida na Etapa 2 (Render Free Tier) não oferece *workers* em segundo plano nem servidor Redis gerenciado sem custo. Optou-se por manter a arquitetura modular interna (`ServicoImportacao` e `transaction.atomic()`), mas executando a importação de forma síncrona com retorno `201 Created`.
* **Criação de endpoints para importação da planilha de execução (`HU-018`) para alimentar a trava de kits:** Não pôde ser aceita a inclusão de novos endpoints de execução/auditoria financeira para não extrapolar o limite recomendado de 3 a 5 histórias prioritárias no MVP, mantendo o foco no recorte definido.
* **Endpoint de renovação de token (`POST /api/v1/auth/refresh/`) com rotação em banco:** Não foi aceito por adicionar complexidade de gestão de sessões desnecessária para o protótipo, sendo suficiente o token de turno único (8h) descartado no cliente ao acionar o logout.

---

## 5. Tabela Consolidada de Registro (Modelo da Disciplina)

| Data | Ferramenta (plano) | Etapa | Prompt (resumo) | Resultado e verificação | Ajustes manuais |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 15/11/2026 | Gemini (gratuito) | 1. Pacote de Contexto | Revisar `contrato-api.md` contra `historias-priorizadas.md` apontando endpoints faltantes ou inconsistentes. | Apontou 3 endpoints faltantes (`equipes`, `auditoria`, `logout`) e 6 inconsistências de payload/paginação/status HTTP; sugestões verificadas contra o Projeto Arquitetural e os diagramas C4. | Incorporados os endpoints de consulta, padronizado retorno `201 Created` síncrono para o Render gratuito, adicionada paginação e descartado fluxo assíncrono Celery/Redis e `HU-018` no escopo do MVP. |
| 16/11/2026 | Gemini (gratuito) | 2. Esqueleto ambulante | Gerar configuração inicial do Django + DRF com rota `GET /health` (`SELECT 1;`) conectada ao PostgreSQL Neon e frontend React + TypeScript com Vite | Estrutura criada localmente e validada com retorno `HTTP 200 OK` antes do deploy | Ajustado `DATABASE_URL` no `.env` local e configurado `.gitignore` para bloquear credenciais |
| 16/11/2026 | Gemini (gratuito) | 2. Esqueleto ambulante | Diagnosticar falha de build no Render (`psycopg-binary`) e configurar comunicação CORS entre Vercel e Render | Identificada incompatibilidade do `psycopg-binary==3.2.3` com Python 3.14 no Render e necessidade de liberar origem da Vercel | Atualizado `psycopg[binary]==3.3.9` no `requirements.txt`, fixada versão do Python no Render e atualizado `CORS_ALLOWED_ORIGINS` com a URL da Vercel |