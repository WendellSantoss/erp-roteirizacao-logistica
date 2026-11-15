# GeniOS - ERP Roteirização Logística

**Sistema ERP Operacional para Roteirização, Controle Logístico e Auditoria de Contratos**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow.svg)](#16-roadmap)
[![Versão](https://img.shields.io/badge/versão-1.0.0-informational)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#12-padrão-de-contribuição)

---

## Equipe

Projeto desenvolvido por:

| Integrante                |
|----------------------------|
| Ana Beatriz da Silva        |
| Deivisson da Silva Rocha    |
| Felipe de Almeida Silva     |
| Wendell dos Santos          |


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
11. [Instalação e Execução](#11-instalação-e-execução)
12. [Padrão de Contribuição](#12-padrão-de-contribuição)
13. [Testes](#13-testes)
14. [Segurança e Conformidade](#14-segurança-e-conformidade)
15. [Indicadores e Relatórios (KPIs)](#15-indicadores-e-relatórios-kpis)
16. [Roadmap](#16-roadmap)
17. [Perguntas Frequentes (FAQ)](#17-perguntas-frequentes-faq)
18. [Glossário](#18-glossário)
19. [Equipe](#19-equipe)
20. [Licença](#20-licença)

---

## 1. Visão Geral

O **ERP Roteirização Logística** é uma solução de gestão empresarial (ERP) voltada para empresas do setor de transporte e logística, integrando três frentes operacionais em uma única plataforma:

- **Roteirização**: planejamento e otimização de rotas de entrega e coleta;
- **Controle Logístico**: gestão de frota, motoristas, cargas e status de entregas em tempo real;
- **Auditoria de Contratos**: acompanhamento da conformidade de contratos firmados com clientes e fornecedores.

O sistema centraliza informações que tradicionalmente ficam dispersas entre planilhas, sistemas isolados e controles manuais, proporcionando maior visibilidade operacional, rastreabilidade de processos e apoio à tomada de decisão gerencial.

Este projeto foi desenvolvido no contexto acadêmico/técnico, aplicando conceitos de engenharia de software, modelagem de banco de dados, arquitetura em camadas e boas práticas de desenvolvimento colaborativo.

## 2. Contexto e Justificativa

Empresas do setor logístico frequentemente enfrentam três problemas recorrentes:

1. **Ineficiência no planejamento de rotas**, gerando custos elevados com combustível, tempo ocioso e atrasos nas entregas;
2. **Falta de visibilidade sobre a frota e as cargas**, dificultando o acompanhamento em tempo real do status das operações;
3. **Ausência de controle sistemático sobre contratos**, resultando em vencimentos não identificados, cláusulas não cumpridas e riscos jurídicos e financeiros.

O ERP Roteirização Logística propõe endereçar esses três problemas de forma integrada, eliminando a fragmentação de informações e reduzindo a dependência de controles manuais.

## 3. Objetivos do Projeto

### 3.1 Objetivo Geral

Desenvolver um sistema ERP que integre roteirização, controle logístico e auditoria de contratos, oferecendo uma plataforma única para gestão operacional do setor de transporte e logística.

### 3.2 Objetivos Específicos

- Reduzir custos operacionais por meio da otimização de rotas de entrega e coleta;
- Aumentar a eficiência do controle de frota, motoristas e cargas;
- Automatizar processos de auditoria contratual, reduzindo riscos de não conformidade;
- Centralizar dados operacionais em uma base única e confiável;
- Disponibilizar indicadores gerenciais (KPIs) para apoio à tomada de decisão;
- Garantir rastreabilidade e histórico auditável de todas as operações registradas;
- Implementar controle de acesso por perfil de usuário, assegurando segurança da informação.

## 4. Público-Alvo e Perfis de Usuário

O sistema é destinado a empresas de transporte, distribuição e logística de pequeno, médio e grande porte. Os principais perfis de usuário previstos são:

| Perfil        | Descrição das Responsabilidades                                                             |
|---------------|-----------------------------------------------------------------------------------------------|
| Administrador | Gestão completa do sistema, cadastro de usuários, configurações gerais e acesso a todos os módulos. |
| Operador      | Responsável pelo cadastro e acompanhamento de rotas, entregas, veículos e motoristas.          |
| Auditor       | Responsável pela análise de contratos, verificação de conformidade e emissão de relatórios de auditoria. |
| Motorista (consulta) | Acesso restrito para consulta de rotas e entregas atribuídas (perfil opcional, conforme evolução do projeto). |

## 5. Requisitos do Sistema

### 5.1 Requisitos Funcionais

| Código  | Descrição                                                                 |
|---------|------------------------------------------------------------------------------|
| RF01    | O sistema deve permitir o cadastro de rotas com pontos de coleta e entrega.  |
| RF02    | O sistema deve calcular rotas otimizadas por distância e tempo estimado.     |
| RF03    | O sistema deve permitir a reprogramação de rotas em caso de imprevistos.     |
| RF04    | O sistema deve permitir o cadastro e gestão de veículos da frota.            |
| RF05    | O sistema deve permitir o cadastro de motoristas e seu vínculo com veículos e rotas. |
| RF06    | O sistema deve registrar e atualizar o status de cada entrega.               |
| RF07    | O sistema deve permitir o controle de estoque e movimentação de cargas.      |
| RF08    | O sistema deve permitir o cadastro de contratos com clientes e fornecedores. |
| RF09    | O sistema deve emitir alertas automáticos de vencimento contratual.         |
| RF10    | O sistema deve permitir o registro de auditorias e não conformidades.       |
| RF11    | O sistema deve gerar relatórios de conformidade contratual por período.      |
| RF12    | O sistema deve autenticar usuários e controlar o acesso por perfil.         |
| RF13    | O sistema deve exibir um dashboard com indicadores operacionais.            |
| RF14    | O sistema deve permitir a exportação de relatórios em PDF e Excel.          |
| RF15    | O sistema deve registrar um log de auditoria das ações realizadas por usuário. |

### 5.2 Requisitos Não Funcionais

| Código   | Descrição                                                                      |
|----------|-----------------------------------------------------------------------------------|
| RNF01    | O sistema deve responder às requisições em tempo aceitável (abaixo de 2 segundos em operações comuns). |
| RNF02    | O sistema deve garantir a integridade dos dados armazenados.                      |
| RNF03    | O sistema deve possuir controle de acesso baseado em perfis (RBAC).               |
| RNF04    | O sistema deve armazenar senhas de forma criptografada.                          |
| RNF05    | O sistema deve ser compatível com os principais navegadores web (Chrome, Firefox, Edge). |
| RNF06    | O sistema deve seguir arquitetura em camadas para facilitar manutenção e testes.  |
| RNF07    | O sistema deve manter logs de auditoria para fins de rastreabilidade.             |
| RNF08    | O sistema deve ser escalável para suportar aumento de volume de dados e usuários. |
| RNF09    | O código-fonte deve seguir padrões de nomenclatura e organização definidos pela equipe. |
| RNF10    | O sistema deve possuir documentação técnica atualizada (este README e arquivos em `docs/`). |

## 6. Escopo Funcional Detalhado

### 6.1 Módulo de Roteirização

- Cadastro de rotas, pontos de entrega/coleta e regiões de atendimento;
- Cálculo de rotas otimizadas (menor distância/tempo);
- Definição de janelas de horário para entregas;
- Visualização de rotas em mapa;
- Reprogramação dinâmica de rotas em caso de imprevistos (trânsito, avarias, cancelamentos);
- Histórico de rotas executadas, com tempo real vs. tempo estimado.

### 6.2 Módulo de Controle Logístico

- Cadastro e gestão de veículos da frota (placa, capacidade, tipo, status de manutenção);
- Cadastro de motoristas e vínculo com veículos/rotas;
- Controle de status de entregas (pendente, em trânsito, entregue, devolvido, cancelado);
- Gestão de estoque e movimentação de cargas entre pontos de distribuição;
- Histórico de manutenção preventiva e corretiva dos veículos;
- Alertas de manutenção programada.

### 6.3 Módulo de Auditoria de Contratos

- Cadastro de contratos com clientes e fornecedores, incluindo vigência, cláusulas e valores;
- Controle de status contratual (ativo, em renovação, encerrado, suspenso);
- Alertas de vencimento e renovação de contratos;
- Registro de auditorias periódicas e identificação de não conformidades;
- Registro de ações corretivas vinculadas a não conformidades identificadas;
- Geração de relatórios de conformidade contratual por cliente, fornecedor ou período.

### 6.4 Módulo Administrativo e de Segurança

- Autenticação e controle de acesso por perfil de usuário (administrador, operador, auditor);
- Dashboard com indicadores operacionais consolidados (KPIs de rotas, frota e contratos);
- Emissão de relatórios gerenciais em PDF e Excel;
- Log de auditoria de todas as ações relevantes realizadas no sistema;
- Gestão de usuários, permissões e redefinição de senhas.

## 7. Arquitetura do Sistema

### 7.1 Visão em Camadas

O sistema adota uma arquitetura em camadas, separando interface, regras de negócio e persistência de dados, o que favorece manutenibilidade, testabilidade e evolução independente de cada camada:

```
┌───────────────────────────────┐
│      Front-end (Interface)     │
│  Dashboard, formulários, mapas │
└───────────────┬─────────────────┘
                │ HTTP / REST API
┌───────────────▼─────────────────┐
│       Back-end (API/Serviços)   │
│  Regras de negócio, autenticação│
│  Roteirização, auditoria        │
└───────────────┬─────────────────┘
                │ ORM / Queries
┌───────────────▼─────────────────┐
│      Banco de Dados (SGBD)       │
│  Rotas, veículos, contratos,     │
│  usuários, auditorias, etc.      │
└───────────────────────────────────┘
```

### 7.2 Fluxo de Dados

1. O usuário interage com a interface (dashboard, formulários de cadastro, telas de acompanhamento);
2. As requisições são enviadas via API REST para o back-end;
3. O back-end aplica as regras de negócio (validações, cálculos de rota, verificação de conformidade contratual);
4. Os dados são persistidos ou consultados no banco de dados via camada de acesso a dados (ORM);
5. A resposta é retornada ao front-end, atualizando a interface do usuário.

## 8. Tecnologias Utilizadas

> Seção a ser atualizada conforme definição final da stack pela equipe.

| Camada              | Tecnologia prevista                          |
|---------------------|-------------------------------------------------|
| Back-end            | A definir (ex.: Java com Spring Boot / Node.js com Express / Python com Django) |
| Front-end           | A definir (ex.: React / Angular / HTML, CSS, JavaScript) |
| Banco de Dados      | A definir (ex.: MySQL / PostgreSQL / SQL Server) |
| Controle de versão  | Git e GitHub                                     |
| Modelagem de dados  | Diagrama Entidade-Relacionamento (DER), UML       |
| Gestão de projeto   | Kanban (ex.: Trello, GitHub Projects, Notion)     |
| Documentação        | Markdown                                          |

## 9. Modelagem de Dados

### 9.1 Dicionário de Entidades

| Entidade    | Descrição                                                        |
|-------------|----------------------------------------------------------------------|
| Usuario     | Usuários do sistema e seus perfis de acesso (administrador, operador, auditor). |
| Motorista   | Motoristas cadastrados, vinculados a veículos e rotas.                |
| Veiculo     | Frota disponível para operação, com dados de capacidade e manutenção. |
| Rota        | Trajetos planejados, com pontos de parada e janelas de horário.        |
| Entrega     | Registros de entrega/coleta associados a uma rota específica.          |
| Cliente     | Clientes atendidos pela operação logística.                            |
| Fornecedor  | Fornecedores vinculados a contratos de prestação de serviço.            |
| Contrato    | Contratos firmados com clientes e fornecedores, com vigência e cláusulas. |
| Auditoria   | Registros de conformidade e não conformidade contratual, com ações corretivas. |

### 9.2 Relacionamentos Principais

- Um **Motorista** pode estar vinculado a múltiplos **Veículos** ao longo do tempo, mas a apenas um por vez em cada **Rota**;
- Uma **Rota** possui múltiplas **Entregas**, cada uma vinculada a um **Cliente**;
- Um **Contrato** está vinculado a um **Cliente** ou **Fornecedor**, e pode gerar múltiplos registros de **Auditoria**;
- Cada **Auditoria** pode gerar ações corretivas registradas e vinculadas ao contrato correspondente.

> O diagrama entidade-relacionamento (DER) completo deve ser mantido em `database/diagramas/`.

## 10. Estrutura do Repositório

```
erp-roteirizacao-logistica/
│
├── backend/                  # API e regras de negócio
│   ├── src/
│   ├── config/
│   └── tests/
│
├── frontend/                  # Interface do usuário
│   ├── src/
│   ├── public/
│   └── assets/
│
├── database/                   # Scripts SQL, migrações e diagramas
│   ├── migrations/
│   └── diagramas/
│
├── docs/                        # Documentação complementar do projeto
│   ├── requisitos.md
│   └── arquitetura.md
│
├── .gitignore
├── LICENSE
└── README.md
```

## 11. Instalação e Execução

### 11.1 Pré-requisitos

- Git instalado;
- Runtime/linguagem definida pela equipe (ex.: Node.js, JDK, Python);
- SGBD configurado (ex.: MySQL, PostgreSQL);
- Gerenciador de pacotes correspondente à stack escolhida (ex.: npm, pip, maven).

### 11.2 Passo a Passo

```bash
# 1. Clonar o repositório
git clone https://github.com/WendellSantoss/erp-roteirizacao-logistica.git

# 2. Acessar a pasta do projeto
cd erp-roteirizacao-logistica

# 3. Instalar as dependências
npm install

# 4. Configurar as variáveis de ambiente
cp .env.example .env

# 5. Executar as migrações do banco de dados
npm run migrate

# 6. Iniciar a aplicação
npm start
```

> Os comandos acima devem ser ajustados conforme a stack tecnológica final adotada pela equipe.

### 11.3 Variáveis de Ambiente

| Variável       | Descrição                                  |
|----------------|-------------------------------------------------|
| `DB_HOST`      | Endereço do servidor de banco de dados          |
| `DB_PORT`      | Porta de conexão do banco de dados              |
| `DB_USER`      | Usuário de acesso ao banco de dados             |
| `DB_PASSWORD`  | Senha de acesso ao banco de dados               |
| `DB_NAME`      | Nome do banco de dados                          |
| `APP_PORT`     | Porta em que a aplicação será executada         |
| `JWT_SECRET`   | Chave secreta utilizada para geração de tokens de autenticação |

## 12. Padrão de Contribuição

### 12.1 Fluxo de Branches

1. Realize um fork do repositório (caso não seja colaborador direto);
2. Crie uma branch a partir de `main` com nome descritivo: `feature/nome-da-feature`, `fix/nome-do-bug` ou `docs/nome-da-documentacao`;
3. Desenvolva e teste as alterações localmente;
4. Envie a branch para o repositório remoto;
5. Abra um Pull Request descrevendo claramente as alterações realizadas;
6. Aguarde revisão de ao menos um outro integrante da equipe antes do merge.

### 12.2 Padrão de Commits

Utilize o padrão `tipo: descrição breve`, seguindo os tipos abaixo:

| Tipo       | Uso                                                        |
|------------|-------------------------------------------------------------|
| `feat`     | Nova funcionalidade                                          |
| `fix`      | Correção de bug                                              |
| `docs`     | Alterações na documentação                                   |
| `refactor` | Refatoração de código sem alteração de comportamento         |
| `test`     | Adição ou ajuste de testes                                   |
| `chore`    | Tarefas de manutenção (configuração, dependências, etc.)     |

Exemplo: `feat: adiciona cálculo de rota otimizada por distância`

## 13. Testes

- **Testes unitários**: cobrindo regras de negócio críticas (cálculo de rotas, validações de contrato, controle de status de entrega);
- **Testes de integração**: validando a comunicação entre back-end e banco de dados;
- **Testes manuais**: roteiro de testes funcionais documentado em `docs/` para validação das principais jornadas de uso (cadastro de rota, registro de entrega, cadastro e auditoria de contrato).

```bash
# Exemplo de execução de testes (ajustar conforme stack adotada)
npm test
```

## 14. Segurança e Conformidade

- Autenticação de usuários com armazenamento de senhas criptografadas;
- Controle de acesso baseado em perfis (RBAC), restringindo funcionalidades conforme o papel do usuário;
- Log de auditoria para todas as ações relevantes realizadas no sistema (criação, edição e exclusão de registros);
- Validação de dados de entrada em todas as camadas para prevenir inconsistências e vulnerabilidades comuns (ex.: injeção de SQL);
- Boas práticas de proteção de variáveis sensíveis, mantendo credenciais fora do controle de versão (uso de `.env`).

## 15. Indicadores e Relatórios (KPIs)

O dashboard administrativo deve consolidar, entre outros, os seguintes indicadores:

- Número de rotas concluídas no período;
- Tempo médio de entrega por rota;
- Percentual de entregas realizadas dentro do prazo;
- Custo médio por rota (combustível, manutenção);
- Número de contratos ativos, em renovação e encerrados;
- Número de não conformidades identificadas em auditorias no período;
- Percentual de conformidade contratual geral.

## 16. Roadmap

- [x] Levantamento de requisitos funcionais e não funcionais
- [ ] Modelagem do banco de dados
- [ ] Desenvolvimento do módulo de roteirização
- [ ] Desenvolvimento do módulo de controle logístico
- [ ] Desenvolvimento do módulo de auditoria de contratos
- [ ] Implementação de autenticação e perfis de acesso
- [ ] Implementação do dashboard de indicadores
- [ ] Testes automatizados (unitários e de integração)
- [ ] Documentação técnica complementar (`docs/`)
- [ ] Deploy em ambiente de homologação
- [ ] Deploy em ambiente de produção

## 17. Perguntas Frequentes (FAQ)

**O sistema pode ser utilizado por empresas de qualquer porte?**
Sim, a arquitetura foi pensada para ser escalável, atendendo desde pequenas transportadoras até operações de maior volume.

**É necessário conexão com serviços externos de mapas?**
Dependendo da estratégia de roteirização adotada, pode ser necessária integração com APIs de geolocalização e cálculo de rotas (a definir pela equipe).

**O sistema substitui o uso de planilhas de controle logístico?**
Sim, esse é um dos objetivos centrais do projeto: centralizar em uma única plataforma informações antes dispersas em planilhas e controles manuais.

## 18. Glossário

| Termo         | Definição                                                                 |
|---------------|--------------------------------------------------------------------------|
| ERP           | Enterprise Resource Planning — sistema integrado de gestão empresarial.  |
| Roteirização  | Processo de planejamento e otimização de rotas de entrega/coleta.       |
| KPI           | Key Performance Indicator — indicador-chave de desempenho.               |
| RBAC          | Role-Based Access Control — controle de acesso baseado em papéis/perfis. |
| DER           | Diagrama Entidade-Relacionamento — representação da modelagem de dados. |
| Não conformidade | Situação em que uma cláusula contratual ou processo não é cumprido conforme o previsto. |

## 19. Equipe

Projeto desenvolvido por:

| Integrante                |
|----------------------------|
| Ana Beatriz da Silva        |
| Deivisson da Silva Rocha    |
| Felipe de Almeida Silva     |
| Wendell dos Santos          |

## 20. Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

<p align="center">Desenvolvido para otimizar a logística, o controle operacional e a conformidade contratual.</p>
