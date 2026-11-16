# Diagramas Arquiteturais — Modelo C4 (GeniOS)

Esta pasta contém os diagramas arquiteturais exportados do MVP do **GeniOS**, materializando a decisão do **ADR-001** (Monólito Modular com Processamento Assíncrono):

1. **`c4-nivel1-contexto.jpg`** — **Nível 1 (Contexto):** Apresenta os seis perfis de usuários do GeniOS e os cinco sistemas externos (GSAN por arquivo `.xlsx`, Portal GSAN de unidades, Automação RPA, Serviço de Mapas e Serviço de IA).
2. **`c4-nivel2-containers.jpg`** — **Nível 2 (Contêineres):** Detalha a Aplicação Web SPA (React + TypeScript), a API de Aplicação (Python, Django + DRF), o Worker Assíncrono (Celery), a Fila (Redis), o Banco de Dados (PostgreSQL + PostGIS) e o Armazenamento de Arquivos.
3. **`c4-nivel3-componentes.jpg`** — **Nível 3 (Componentes):** Abre a API de Aplicação com foco no **Módulo Importação** (`app importacao`) e sua interação com o **Núcleo compartilhado** (`app nucleo`).
4. **`c4-nivel4-codigo.jpg`** — **Nível 4 (Código):** Diagrama de classes do módulo de Importação e do Núcleo (`ImportacaoViewSet`, `ServicoImportacao`, `LeitorPlanilhaGSAN`, `FiltroEscopo`, `UpsertOrdensServico`, `CicloDeVidaOS` e `TrilhaAuditoria`).

---

## Regras de dependência entre módulos

No ADR-001, o grupo aceitou o risco de o acoplamento entre módulos crescer com o tempo. As regras abaixo mantêm a separação e podem ser verificadas automaticamente na integração contínua (por exemplo, com a ferramenta `import-linter`):

1. **Endpoints só traduzem HTTP; toda regra fica em `services.py` (`HU-F03`).** Assim a tela, o Worker e o Assistente executam exatamente as mesmas regras (`RN-21`).
2. **Um módulo não grava nas tabelas de outro:** usa o serviço público do módulo dono do dado.
3. **O estado da OS só muda pelo Ciclo de Vida da OS (`HU-F11`, `CA04`).**
4. **Toda alteração de dado operacional ou financeiro grava a trilha na mesma transação:** sem registro, sem alteração (`HU-045`).
5. **O Núcleo não depende de nenhum módulo de negócio;** as dependências apontam sempre dos módulos para o Núcleo.