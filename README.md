# GeniOS — ERP Roteirização Logística

**Sistema ERP Operacional para Roteirização, Controle Logístico e Auditoria de Contratos**

[![Sistema: ERP](https://img.shields.io/badge/Sistema-ERP-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-%20finalizado-yellow.svg)](#16-roadmap)
[![Versão](https://img.shields.io/badge/versão-1.0.0-informational)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#12-padrão-de-contribuição)

---

## Links do Protótipo Publicado (Nuvem)

* **Frontend (Vercel):** https://erp-roteirizacao-logistica-so5e.vercel.app
* **Backend / Health Check (Render):** https://genios-api-kruh.onrender.com/health

> ⚠️ **Aviso sobre tempo de resposta (Plano Gratuito Render):** O servidor backend está hospedado no plano gratuito do Render e hiberna automaticamente após períodos de inatividade. Por isso, **o primeiro acesso após um período ocioso pode levar cerca de 50 a 60 segundos (~1 minuto)** para responder enquanto o contêiner é reativado.

---

## Equipe

Projeto desenvolvido por:

| Integrante                 |
|----------------------------|
| Ana Beatriz da Silva       |
| Deivisson da Silva Rocha   |
| Felipe de Almeida Silva    |
| Wendell dos Santos         |

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Contexto e Justificativa](#2-contexto-e-justificativa)
3. [Objetivos do Projeto](#3-objetivos-do-projeto)
4. [Público-Alvo e Perfis de Usuário](#4-público-alvo-e-perfis-de-usuário)
5. [Requisitos do Sistema](#5-requisitos-do-sistema)
6. [Escopo Funcional Detalhado](#6-escopo-funcional-detalhado)
7. [Arquitetura do Sistema](#7-arquitetura-do-sistema)
8. [Tecnologias Utilizadas](#8-tecnologias-utilizadas)
9. [Modelagem de Dados](#9-modelagem-de-dados)
10. [Estrutura do Repositório](#10-estrutura-do-repositório)
11. [Instalação e Execução Local](#11-instalação-e-execução-local)
12. [Padrão de Contribuição](#12-padrão-de-contribuição)
13. [Testes e Validação](#13-testes-e-validação)
14. [Segurança e Conformidade](#14-segurança-e-conformidade)
15. [Indicadores e Relatórios (KPIs)](#15-indicadores-e-relatórios-kpis)
16. [Roadmap](#16-roadmap)
17. [Perguntas Frequentes (FAQ)](#17-perguntas-frequentes-faq)
18. [Glossário](#18-glossário)

---

## 1. Visão Geral

O **GeniOS (ERP Roteirização Logística)** é uma solução de gestão empresarial (ERP) voltada para empresas do setor de transporte, saneamento/serviço de campo e logística, integrando três frentes operacionais em uma única plataforma:

- **Roteirização**: planejamento e otimização de rotas de entrega, coleta e atendimento de Ordens de Serviço (OS);
- **Controle Logístico**: gestão de frota, equipes/motoristas, kits de materiais, cargas e status de entregas em tempo real;
- **Auditoria de Contratos**: acompanhamento da conformidade de contratos firmados com clientes e fornecedores, incluindo travas de histórico e rastreabilidade.

O sistema centraliza informações que tradicionalmente ficam dispersas entre planilhas, sistemas legados (como GSAN) e controles manuais, proporcionando maior visibilidade operacional, rastreabilidade de processos e apoio à tomada de decisão gerencial.

Este projeto foi desenvolvido no contexto acadêmico/técnico com apoio de IA, aplicando conceitos de engenharia de software, modelagem C4, arquitetura em camadas e boas práticas de desenvolvimento colaborativo.

## 2. Contexto e Justificativa

Empresas do setor logístico frequentemente enfrentam três problemas recorrentes:

1. **Ineficiência no planejamento de rotas**, gerando custos elevados com combustível, tempo ocioso e atrasos nas entregas/execuções;
2. **Falta de visibilidade sobre a frota, equipes e cargas**, dificultando o acompanhamento em tempo real do status das operações;
3. **Ausência de controle sistemático sobre contratos**, resultando em vencimentos não identificados, cláusulas não cumpridas e riscos jurídicos e financeiros.

O **GeniOS** propõe endereçar esses três problemas de forma integrada, eliminando a fragmentação de informações e reduzindo a dependência de controles manuais.

## 3. Objetivos do Projeto

### 3.1 Objetivo Geral

Desenvolver um sistema ERP que integre roteirização, controle logístico e auditoria de contratos, oferecendo uma plataforma única para gestão operacional do setor de transporte e logísticas.

### 3.2 Objetivos Específicos

- Reduzir custos operacionais por meio da otimização de rotas de entrega e coleta;
- Aumentar a eficiência do controle de frota, equipes, motoristas e cargas;
- Automatizar processos de auditoria contratual, reduzindo riscos de não conformidade;
- Centralizar dados operacionais em uma base única e confiável;
- Disponibilizar indicadores gerenciais (KPIs) para apoio à tomada de decisão;
- Garantir rastreabilidade e histórico auditável de todas as operações registradas;
- Implementar controle de acesso por perfil de usuário, assegurando segurança da informação.

## 4. Público-Alvo e Perfis de Usuário

| Perfil               | Descrição das Responsabilidades                                                                 |
|----------------------|-------------------------------------------------------------------------------------------------|
| Administrador        | Gestão completa do sistema, cadastro de usuários, configurações gerais e acesso a todos os polos/módulos. |
| Operador             | Responsável pela importação de dados, cadastro e acompanhamento de rotas, entregas, equipes e veículos. |
| Auditor              | Responsável pela análise de contratos, verificação de conformidade, histórico de kits e emissão de relatórios. |
| Motorista (consulta) | Acesso restrito para consulta de rotas e entregas atribuídas (perfil previsto na evolução do projeto). |

## 5. Requisitos do Sistema

### 5.1 Requisitos Funcionais

| Código | Descrição                                                                            |
|--------|--------------------------------------------------------------------------------------|
| RF01   | O sistema deve permitir o cadastro de rotas com pontos de coleta e entrega.          |
| RF02   | O sistema deve calcular rotas otimizadas por distância e tempo estimado.             |
| RF03   | O sistema deve permitir a reprogramação de rotas em caso de imprevistos.             |
| RF04   | O sistema deve permitir o cadastro e gestão de veículos da frota.                    |
| RF05   | O sistema deve permitir o cadastro de motoristas/equipes e seu vínculo com veículos e rotas. |
| RF06   | O sistema deve registrar e atualizar o status de cada entrega / Ordem de Serviço.    |
| RF07   | O sistema deve permitir o controle de estoque, kits e movimentação de cargas.        |
| RF08   | O sistema deve permitir o cadastro de contratos com clientes e fornecedores.         |
| RF09   | O sistema deve emitir alertas automáticos de vencimento contratual.                 |
| RF10   | O sistema deve permitir o registro de auditorias e não conformidades.                |
| RF11   | O sistema deve gerar relatórios de conformidade contratual por período.              |
| RF12   | O sistema deve autenticar usuários e controlar o acesso por perfil e polo.           |
| RF13   | O sistema deve exibir um dashboard com indicadores operacionais.                     |
| RF14   | O sistema deve permitir a exportação de relatórios em PDF e Excel.                   |
| RF15   | O sistema deve registrar um log de auditoria das ações realizadas por usuário.       |

### 5.2 Requisitos Não Funcionais

| Código | Descrição                                                                                 |
|--------|-------------------------------------------------------------------------------------------|
| RNF01  | O sistema deve responder às requisições em tempo aceitável (abaixo de 2 segundos em operações comuns, após o warm-up da instância). |
| RNF02  | O sistema deve garantir a integridade transacional dos dados armazenados.                 |
| RNF03  | O sistema deve possuir controle de acesso baseado em perfis (RBAC) e filtro global por polo. |
| RNF04  | O sistema deve armazenar senhas de forma criptografada.                                   |
| RNF05  | O sistema deve ser compatível com os principais navegadores web (Chrome, Firefox, Edge).  |
| RNF06  | O sistema deve seguir arquitetura de Monólito Modular em camadas para facilitar manutenção e testes. |
| RNF07  | O sistema deve manter logs de auditoria imutáveis para fins de rastreabilidade.           |
| RNF08  | O sistema deve ser escalável para suportar aumento de volume de dados e usuários.         |
| RNF09  | O código-fonte deve seguir padrões de nomenclatura e organização definidos pela equipe.   |
| RNF10  | O sistema deve possuir documentação técnica atualizada (este README e arquivos em `docs/`). |

## 6. Escopo Funcional Detalhado

### 6.1 Módulo de Roteirização

- Importação e validação de planilhas operacionais (GSAN) com upsert transacional;
- Cadastro de rotas, pontos de entrega/coleta e regiões/polos de atendimento;
- Cálculo de rotas otimizadas (menor distância/tempo);
- Visualização de rotas e reprogramação dinâmica em caso de imprevistos;
- Histórico de rotas executadas, com tempo real vs. tempo estimado.

### 6.2 Módulo de Controle Logístico

- Cadastro e gestão de veículos da frota (placa, capacidade, tipo, status de manutenção);
- Cadastro de motoristas/equipes e vínculo com veículos/rotas;
- Controle de status de entregas e Ordens de Serviço pendentes;
- Gestão de estoque, kits de materiais e movimentação de cargas;
- Histórico e alertas de manutenção preventiva e corretiva dos veículos.

### 6.3 Módulo de Auditoria de Contratos

- Cadastro de contratos com clientes e fornecedores, incluindo vigência, cláusulas e valores;
- Controle de status contratual (ativo, em renovação, encerrado, suspenso);
- Trava de histórico de kits utilizados em OS concluídas;
- Registro de auditorias periódicas, identificação de não conformidades e ações corretivas;
- Geração de relatórios de conformidade contratual por cliente, fornecedor ou período.

### 6.4 Módulo Administrativo e de Segurança

- Autenticação via token e controle de acesso por perfil de usuário (administrador, operador, auditor) e filtro por polo;
- Dashboard com indicadores operacionais consolidados (KPIs de rotas, frota e contratos);
- Log de auditoria de todas as ações relevantes realizadas no sistema.

## 7. Arquitetura do Sistema

### 7.1 Visão em Camadas e Hospedagem (ADR-001)

O sistema adota a arquitetura de **Monólito Modular** (detalhada em `docs/adr/ADR-001-arquitetura-mvp.md`), separando a SPA frontend da API REST backend e do banco gerenciado na nuvem:

```
┌─────────────────────────────────────────┐
│     Front-end SPA (Vercel)              │
│     React + TypeScript + Vite           │
└────────────────────┬────────────────────┘
                     │ HTTPS / REST API (JSON)
┌────────────────────▼────────────────────┐
│     Back-end API REST (Render)          │
│     Python + Django + DRF               │
│     (Monólito Modular: núcleo/rotas)    │
└────────────────────┬────────────────────┘
                     │ PostgreSQL (SSL)
┌────────────────────▼────────────────────┐
│     Banco de Dados (Neon)               │
│     PostgreSQL Gerenciado na Nuvem      │
└─────────────────────────────────────────┘
```

### 7.2 Fluxo de Dados

1. O usuário interage com a interface web (SPA hospedada na Vercel);
2. As requisições são enviadas via API REST (HTTPS/JSON) para o back-end Django no Render;
3. O back-end aplica as regras de negócio (autenticação, validações, importação transacional, cálculo de rotas e auditoria);
4. Os dados são persistidos ou consultados no PostgreSQL hospedado no Neon via ORM do Django;
5. A resposta é retornada ao front-end, atualizando a interface do usuário.

## 8. Tecnologias Utilizadas

Conforme definido no **ADR-001** (`docs/adr/ADR-001-arquitetura-mvp.md`):

| Camada             | Tecnologia adotada                                      |
|--------------------|---------------------------------------------------------|
| Back-end           | Python 3.11+, Django 5.1, Django REST Framework (DRF)   |
| Front-end          | React 19, TypeScript, Vite                              |
| Banco de Dados     | PostgreSQL (hospedado no Neon)                          |
| Hospedagem / Cloud | Vercel (Front-end) e Render (Back-end via Gunicorn)     |
| Controle de versão | Git e GitHub                                            |
| Modelagem          | Modelo C4 (Contexto, Contêineres e Componentes) em `docs/` |
| Gestão de projeto  | GitHub Projects (Kanban)                                |
| Documentação       | Markdown e Architecture Decision Records (ADR)          |

## 9. Modelagem de Dados

O esquema completo, com justificativas, riscos, LGPD e a tabela "história → tabelas lidas/gravadas",
está em **[`docs/banco/modelo-dados.md`](docs/banco/modelo-dados.md)**. Diagrama ER:
[`docs/banco/diagrama-er.png`](docs/banco/diagrama-er.png).

| Módulo | Tabelas | Histórias |
|---|---|---|
| `nucleo` | Polo, PerfilUsuario (+ `auth_user`), Unidade, Equipe, OrdemServico, RegistroAuditoria | HU-019/020, HU-006..008, HU-F11 |
| `importacao` | Importacao, AlertaImportacao | HU-001..004 |
| `almoxarifado` | TipoKit, ExecucaoKit (limite D-1), SaidaKit | HU-016 |

- A OS é identificada por `(numero, polo)` (RN-01) e só tem os campos vindos do GSAN atualizados na reimportação (RN-02).
- A trilha de auditoria é **append-only**: um trigger no PostgreSQL bloqueia UPDATE e DELETE (RNF-16).
- No máximo uma importação em andamento por polo, garantido por índice único parcial.

## 10. Estrutura do Repositório

```
erp-roteirizacao-logistica/
│
├── backend/                     # API REST em Python / Django + DRF
│   ├── config/                  # Configurações do projeto Django (settings, urls, wsgi)
│   ├── nucleo/                  # Núcleo: polos, usuários, OS, auditoria, health check
│   ├── importacao/              # Módulo de importação da planilha GSAN
│   ├── almoxarifado/            # Módulo de kits e trava de histórico
│   ├── dados_demo/              # Seeds fictícios (python manage.py popular_dados_demo)
│   ├── .env.example             # Modelo de variáveis de ambiente do backend
│   ├── .importlinter            # Regras de dependência entre módulos
│   ├── pyproject.toml           # Configuração do ruff (linter e formatter)
│   ├── manage.py                # Utilitário CLI do Django
│   ├── requirements.txt         # Dependências Python
│   └── requirements-dev.txt     # Ferramentas de qualidade (ruff, import-linter)
│
├── frontend/                    # Interface SPA em React + TypeScript (Vite)
│   ├── public/                  # Arquivos estáticos públicos
│   ├── src/                     # servicos/ (única camada com fetch), tipos/, hooks/, componentes/, paginas/
│   ├── vercel.json              # Rewrite da SPA (rotas /pendencias, /importacao... abrem direto)
│   ├── .env.example             # Modelo de variáveis de ambiente do frontend
│   ├── index.html               # Ponto de entrada HTML
│   ├── package.json             # Dependências e scripts Node
│   └── vite.config.ts           # Configuração do Vite
│
├── docs/                        # Pacote de Contexto (Etapa 1)
│   ├── adr/
│   │   └── ADR-001-arquitetura-mvp.md
│   ├── contrato-api.md          # Especificação dos endpoints REST
│   ├── etapa-08-retrospectiva-uso-de-ia.pdf     # Relatório da retrospectiva do uso de IA (Etapa 8)
│   ├── historias-priorizadas.md # Histórias de usuário do MVP
│   ├── banco/                   # Modelo de dados e diagrama ER (Etapa 4)
│   ├── processo/                # Template de prompt (Etapa 3) e relatório das Etapas 5 e 6
│   ├── testes-e-integracao/     # Relatório de integração e testes (Etapa 7)
│   │   └── relatorio-testes-etapa-7.md
│   ├── registro-uso-ia.md       # Log obrigatório de uso de IA nas etapas
│   └── diagramas-c4/            # Diagramas da arquitetura C4
│
├── .github/workflows/           # CI: lint, regras de camadas, testes e build
├── AGENTS.md                    # Guia de código para humanos e IA (Etapa 3)
├── CLAUDE.md                    # Importa o AGENTS.md para o Claude Code
├── .gitignore
├── LICENSE
└── README.md
```

## 11. Instalação e Execução Local

### 11.1 Pré-requisitos

- **Git** instalado;
- **Python 3.11+** instalado;
- **Node.js 20+ (LTS)** e **npm** instalados;
- Uma URL de conexão PostgreSQL válida (ex.: banco gratuito no [Neon](https://neon.tech)).

### 11.2 Passo a Passo

```bash
# 1. Clonar o repositório
git clone [https://github.com/WendellSantoss/erp-roteirizacao-logistica.git](https://github.com/WendellSantoss/erp-roteirizacao-logistica.git)
cd erp-roteirizacao-logistica
```

#### Configurando e rodando o Back-end (`/backend`)
```bash
cd backend

# Copie o arquivo de exemplo e preencha com sua DATABASE_URL real do Neon
cp .env.example .env

# Crie e ative o ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
# source venv/bin/activate

# Instale as dependências, crie as tabelas, popule os dados fictícios e inicie o servidor
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py popular_dados_demo   # usa SENHA_USUARIOS_DEMO do .env
python manage.py runserver

# Verificações do guia de código (AGENTS.md) — rodar antes de cada commit
ruff format --check . && ruff check . && lint-imports && python manage.py test
```
> A API ficará disponível em `http://127.0.0.1:8000` (teste o endpoint `http://127.0.0.1:8000/health`). A documentação interativa (Swagger) fica em `http://127.0.0.1:8000/api/docs/`.

#### Configurando e rodando o Front-end (`/frontend`)
Em outro terminal, a partir da raiz do projeto:
```bash
cd frontend

# Copie o arquivo de exemplo (apontando para [http://127.0.0.1:8000](http://127.0.0.1:8000))
cp .env.example .env

# Instale as dependências e inicie o servidor Vite
npm install
npm run dev

# Verificações do guia de código (AGENTS.md)
npm run format:check && npm run lint && npm test && npm run build
```
> A interface web ficará disponível em `http://localhost:5173`.

### 11.3 Variáveis de Ambiente

| Pasta      | Variável               | Descrição                                                   |
|------------|------------------------|-------------------------------------------------------------|
| `backend`  | `SECRET_KEY`           | Chave secreta do Django                                     |
| `backend`  | `DEBUG`                | `True` em desenvolvimento local, `False` em produção        |
| `backend`  | `DATABASE_URL`         | String de conexão PostgreSQL do Neon (`postgresql://...`)   |
| `backend`  | `ALLOWED_HOSTS`        | Hosts permitidos (ex.: `localhost,127.0.0.1` ou `.onrender.com`) |
| `backend`  | `CORS_ALLOWED_ORIGINS` | URL do front-end autorizada a consumir a API                |
| `backend`  | `SENHA_USUARIOS_DEMO`  | Senha dos usuários fictícios criados pelo seed (só local/demonstração) |
| `frontend` | `VITE_API_URL`         | URL base da API Django (sem barra no final)                 |

## 12. Padrão de Contribuição

### 12.1 Fluxo de Branches

1. Crie uma branch a partir de `main` com nome descritivo: `feature/nome-da-feature`, `fix/nome-do-bug` ou `docs/nome-da-documentacao`;
2. Desenvolva e teste as alterações localmente;
3. Envie a branch para o repositório remoto;
4. Abra um Pull Request descrevendo claramente as alterações realizadas;
5. Aguarde revisão de ao menos um outro integrante da equipe antes do merge.

### 12.2 Padrão de Commits

Utilize o padrão `tipo: descrição breve`, seguindo os tipos abaixo:

| Tipo       | Uso                                                        |
|------------|------------------------------------------------------------|
| `feat`     | Nova funcionalidade                                        |
| `fix`      | Correção de bug                                            |
| `docs`     | Alterações na documentação                                 |
| `refactor` | Refatoração de código sem alteração de comportamento       |
| `test`     | Adição ou ajuste de testes                                 |
| `chore`    | Tarefas de manutenção (configuração, dependências, etc.)   |

Exemplo: `feat: adiciona endpoint de health check conectado ao Neon`

## 13. Testes e Validação

A validação do MVP combina testes automatizados de back-end e front-end, verificação da integração com os serviços publicados e documentação da API.

### 13.1 Teste de integração — Smoke Test (Etapa 2)

- **Fluxo validado:** aplicação publicada na Vercel, API hospedada no Render e banco PostgreSQL no Neon.
- **Verificação:** chamada ao endpoint `GET /health`, que executa `SELECT 1;` no banco de dados.
- **Objetivo:** confirmar que a API está ativa e consegue estabelecer comunicação com o banco de dados.

### 13.2 Testes automatizados do back-end (Etapa 5)

- **Resultado:** 101 testes aprovados em PostgreSQL, executados com `python manage.py test`.
- **Cobertura dos critérios de aceite do MVP:**
  - **HU-019 — Autenticação:** login e bloqueio de acesso;
  - **HU-020 — Controle de acesso:** matriz de permissões, incluindo respostas `403` por célula de acesso;
  - **HU-F11 — Ciclo de vida da OS:** validação de todas as transições de estado;
  - **HU-001 a HU-004 — Importação:** validação do layout, escopo por polo e operação de upsert com garantia de tudo-ou-nada;
  - **HU-006 a HU-008 — Pendências:** cálculo de atraso e tratamento de pendências;
  - **HU-016, CA07 — Kits:** bloqueio de operações com teste real de concorrência.

### 13.3 Testes automatizados do front-end (Etapa 6)

- **Ferramenta:** Vitest, executado por meio de `npm test`.
- **Resultado:** 9 testes aprovados.
- **Validações:** formatos e regras da HU-007 e validação do envio de dados da HU-001.

### 13.4 Build e verificações de qualidade

- Build de produção do front-end concluído com sucesso.
- Verificações de formatação, lint e dependências entre módulos executadas no fluxo de CI.
- Pipeline do GitHub Actions concluído com sucesso para os jobs de front-end, back-end e smoke test publicado.

### 13.5 Documentação da API

A documentação é gerada a partir do código e pode ser consultada pelos seguintes endpoints:

- **Swagger UI:** `/api/docs/`
- **Esquema OpenAPI:** `/api/schema/`

### 13.6 Relatórios e rastreabilidade

O detalhamento dos testes, o mapeamento de história de usuário → endpoint → teste e as decisões técnicas estão documentados em:

- [Etapas 5 e 6 — Implementação e testes](docs/processo/etapas-5-e-6.md)
- [Relatório de testes da Etapa 7](docs/testes-e-integracao/relatorio-testes-etapa-7.md)
- [Roteiro de testes locais com Playwright — Etapa 7](docs/testes-e-integracao/roteiro-playwright-local.md)
- [Índice de evidências da Etapa 7](docs/testes-e-integracao/evidencias/README.md)
- [Workflow de qualidade — GitHub Actions](.github/workflows/qualidade.yml)


## 14. Segurança e Conformidade

- Autenticação de usuários com armazenamento de senhas criptografadas;
- Controle de acesso baseado em perfis (RBAC) e segregação operacional por polo;
- Log de auditoria para todas as ações relevantes realizadas no sistema;
- Proteção rigorosa de credenciais mantendo `.env` fora do controle de versão e versionando apenas `.env.example`.

## 15. Indicadores e Relatórios (KPIs)

O dashboard administrativo consolida os seguintes indicadores:

- Número de rotas e Ordens de Serviço concluídas no período;
- Tempo médio de execução/entrega por rota;
- Percentual de entregas realizadas dentro do prazo;
- Custo médio por rota e consumo de kits;
- Número de contratos ativos, em renovação e encerrados;
- Percentual de conformidade contratual geral.

## 16. Roadmap

- [x] Levantamento de requisitos funcionais e não funcionais
- [x] Pacote de contexto e arquitetura (Histórias priorizadas, ADR-001, Diagramas C4 e Contrato da API)
- [x] Esqueleto ambulante publicado na nuvem (Vercel $\rightarrow$ Render $\rightarrow$ Neon)
- [x] Guia de código, linters e CI (Etapa 3)
- [x] Modelagem do banco de dados, migrations e seeds do MVP (Etapa 4)
- [x] Backend das 5 histórias do MVP com testes e OpenAPI (Etapa 5)
- [x] Frontend das 5 histórias do MVP consumindo a API (Etapa 6)
- [x] Integração, testes ponta a ponta e versão final (Etapa 7)
- [x] Retrospectiva sobre o uso de IA (Etapa 8)
- [x] Roteirização, controle logístico completo, auditoria de contratos e dashboard de KPIs (pós-MVP)

## 17. Perguntas Frequentes (FAQ)

**Por que a primeira requisição demora cerca de 1 minuto?**
Porque o back-end está hospedado no plano gratuito do Render, que coloca o serviço em hibernação após períodos sem acesso. Assim que o contêiner reativa, as respostas seguintes voltam a ser rápidas.

**O sistema substitui o uso de planilhas de controle logístico?**
Sim, esse é um dos objetivos centrais do projeto: centralizar em uma única plataforma informações antes dispersas em planilhas e controles manuais.

## 18. Glossário

| Termo            | Definição                                                                |
|------------------|--------------------------------------------------------------------------|
| ERP              | Enterprise Resource Planning — sistema integrado de gestão empresarial.  |
| Roteirização     | Processo de planejamento e otimização de rotas de entrega/coleta.        |
| KPI              | Key Performance Indicator — indicador-chave de desempenho.               |
| RBAC             | Role-Based Access Control — controle de acesso baseado em papéis/perfis. |
| OS               | Ordem de Serviço operacional vinculada a um polo e uma equipe.           |
| Não conformidade | Situação em que uma cláusula contratual ou processo não é cumprido conforme o previsto. |

---

<p align="center">Desenvolvido para otimizar a logística, o controle operacional e a conformidade contratual.</p>
