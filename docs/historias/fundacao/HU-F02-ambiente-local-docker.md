---
id: HU-F02
titulo: Subir o ambiente local com um comando
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-23]
depende_de: [HU-F01]
---

# HU-F02 — Subir o ambiente local com um comando

## História
Como **desenvolvedor do GeniOS**, quero **subir banco, fila, backend, worker e frontend com um
único comando**, para **começar a trabalhar em qualquer máquina sem instalar dependências uma a
uma**.

## Contexto
Serviços previstos na stack candidata: PostgreSQL com PostGIS (consultas geográficas do mapa),
Redis (fila de tarefas), backend Django, worker Celery e frontend React. A stack definitiva é
registrada no ADR do projeto arquitetural.

## Critérios de aceite
CA01 — Subida completa
Dado uma máquina com Docker e Docker Compose instalados e o repositório clonado
Quando executo `docker compose up` na raiz
Então os serviços `db`, `redis`, `backend`, `worker` e `frontend` ficam saudáveis em até 5 min
na primeira execução, e o frontend abre em `http://localhost:5173`.

CA02 — Banco geográfico
Dado o serviço `db` em execução
Quando executo `SELECT postgis_version();`
Então a extensão PostGIS responde com a versão instalada.

CA03 — Configuração por variável de ambiente
Dado o arquivo `.env.example` versionado
Quando copio para `.env` sem alterar nada
Então o ambiente sobe; nenhum segredo real está versionado no repositório.

CA04 — Recarga ao editar
Dado o ambiente em execução
Quando altero um arquivo em `backend/` ou `frontend/`
Então a mudança aparece sem reiniciar os contêineres.

CA05 — Banco limpo
Dado o ambiente em execução
Quando executo `make reset-db` (ou script equivalente documentado)
Então o banco é recriado, as migrações aplicadas e os dados de exemplo (HU-F09) carregados.

## Fora de escopo
Ambiente de homologação na nuvem (HU-F10).
