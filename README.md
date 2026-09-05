# 🚚 ERP Roteirização Logística

**Sistema ERP Operacional para Roteirização, Controle Logístico e Auditoria de Contratos**

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)
![Versão](https://img.shields.io/badge/versão-1.0.0-informational)

---

## 📑 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Objetivos](#-objetivos)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Modelagem de Dados](#-modelagem-de-dados)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Como Contribuir](#-como-contribuir)
- [Roadmap](#-roadmap)
- [Equipe](#-equipe)
- [Licença](#-licença)

---

## 📌 Sobre o Projeto

O **ERP Roteirização Logística** é um sistema de gestão empresarial (ERP) voltado para empresas do setor de **transporte e logística**, com foco em três pilares principais:

1. **Roteirização** — otimização de rotas de entrega e coleta, reduzindo custos operacionais, tempo de deslocamento e consumo de combustível.
2. **Controle Logístico** — gestão de frotas, motoristas, cargas, estoques e status de entregas em tempo real.
3. **Auditoria de Contratos** — acompanhamento, validação e conformidade de contratos firmados com clientes, fornecedores e transportadoras, garantindo transparência e rastreabilidade de todas as operações.

O sistema foi desenvolvido como projeto acadêmico/técnico com o objetivo de aplicar conceitos de engenharia de software, banco de dados, arquitetura de sistemas e boas práticas de desenvolvimento em um cenário realista do setor logístico.

---

## 🎯 Objetivos

- Reduzir custos operacionais por meio da otimização de rotas;
- Aumentar a eficiência no controle de frotas e cargas;
- Garantir conformidade contratual através de auditoria automatizada;
- Centralizar informações logísticas em um único sistema integrado;
- Gerar relatórios gerenciais para tomada de decisão;
- Proporcionar rastreabilidade total das operações logísticas.

---

## ⚙️ Funcionalidades

### 🗺️ Módulo de Roteirização
- Cadastro de rotas, pontos de entrega/coleta e regiões de atendimento;
- Cálculo de rotas otimizadas (menor distância/tempo);
- Definição de janelas de horário para entregas;
- Visualização de rotas em mapa;
- Reprogramação dinâmica de rotas em caso de imprevistos.

### 📦 Módulo de Controle Logístico
- Cadastro e gestão de veículos e frota;
- Cadastro de motoristas e vínculo com veículos/rotas;
- Controle de status de entregas (pendente, em trânsito, entregue, devolvido);
- Gestão de estoque e movimentação de cargas;
- Histórico de manutenção de veículos.

### 📄 Módulo de Auditoria de Contratos
- Cadastro de contratos com clientes e fornecedores;
- Controle de vigência, cláusulas e valores contratuais;
- Alertas de vencimento e renovação de contratos;
- Registro de auditorias e não conformidades;
- Geração de relatórios de conformidade contratual.

### 👤 Módulo Administrativo
- Autenticação e controle de acesso por perfil de usuário (admin, operador, auditor);
- Dashboard com indicadores (KPIs) operacionais;
- Emissão de relatórios gerenciais em PDF/Excel;
- Log de auditoria de ações realizadas no sistema.

---

## 🏗️ Arquitetura do Sistema

O sistema segue uma arquitetura em camadas, separando responsabilidades entre front-end, back-end e banco de dados, favorecendo manutenibilidade e escalabilidade:

```
┌─────────────────────────────┐
│        Front-end (UI)       │
│   Interface do usuário /    │
│   Dashboard / Formulários   │
└──────────────┬───────────────┘
               │ HTTP / REST API
┌──────────────▼───────────────┐
│         Back-end (API)       │
│  Regras de negócio / Serviços│
│  Autenticação / Roteirização │
└──────────────┬───────────────┘
               │ ORM / Queries
┌──────────────▼───────────────┐
│      Banco de Dados (SGBD)   │
│  Tabelas: rotas, veículos,   │
│  contratos, usuários, etc.   │
└───────────────────────────────┘
```

---

## 🛠️ Tecnologias Utilizadas

> *Ajuste esta seção conforme as tecnologias efetivamente escolhidas pela equipe.*

**Back-end**
- Linguagem: (ex: Java / Python / Node.js)
- Framework: (ex: Spring Boot / Django / Express)

**Front-end**
- (ex: React / Angular / HTML, CSS, JavaScript)

**Banco de Dados**
- (ex: MySQL / PostgreSQL / SQL Server)

**Outras ferramentas**
- Controle de versão: Git & GitHub
- Modelagem: (ex: Diagrama Entidade-Relacionamento, UML)
- Gerenciamento de projeto: (ex: Trello, Notion, GitHub Projects)

---

## 📂 Estrutura de Pastas

```
erp-roteirizacao-logistica/
│
├── backend/                # Código-fonte do servidor/API
│   ├── src/
│   ├── config/
│   └── tests/
│
├── frontend/                # Interface do usuário
│   ├── src/
│   ├── public/
│   └── assets/
│
├── database/                 # Scripts SQL, migrações e modelagem
│   ├── migrations/
│   └── diagramas/
│
├── docs/                     # Documentação do projeto
│   ├── requisitos.md
│   └── arquitetura.md
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🗃️ Modelagem de Dados

Principais entidades previstas no sistema:

| Entidade      | Descrição                                              |
|---------------|----------------------------------------------------------|
| `Usuario`     | Usuários do sistema (admin, operador, auditor)            |
| `Motorista`   | Cadastro de motoristas vinculados às rotas                |
| `Veiculo`     | Frota de veículos disponíveis para entrega                |
| `Rota`        | Trajetos planejados com pontos de parada                   |
| `Entrega`     | Registro de entregas/coletas vinculadas a rotas             |
| `Cliente`     | Clientes atendidos pelo sistema                            |
| `Contrato`    | Contratos firmados com clientes/fornecedores                |
| `Auditoria`   | Registros de auditoria e conformidade dos contratos         |

> Diagramas de entidade-relacionamento (DER) detalhados estão disponíveis em `database/diagramas/`.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Git instalado
- (Runtime/linguagem necessária, ex: Node.js, Java JDK, Python)
- Banco de dados configurado (ex: MySQL/PostgreSQL)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/WendellSantoss/erp-roteirizacao-logistica.git

# 2. Acesse a pasta do projeto
cd erp-roteirizacao-logistica

# 3. Instale as dependências (exemplo para Node.js)
npm install

# 4. Configure as variáveis de ambiente
cp .env.example .env

# 5. Execute as migrações do banco de dados
npm run migrate

# 6. Inicie o servidor
npm start
```

> Ajuste os comandos acima de acordo com a stack tecnológica final adotada pela equipe.

---

## 🤝 Como Contribuir

1. Faça um **fork** do projeto;
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`);
3. Faça o commit das suas alterações (`git commit -m 'Adiciona nova feature'`);
4. Faça o push para a branch (`git push origin feature/nome-da-feature`);
5. Abra um **Pull Request**.

---

## 🗺️ Roadmap

- [x] Levantamento de requisitos
- [x] Modelagem do banco de dados
- [ ] Desenvolvimento do módulo de roteirização
- [ ] Desenvolvimento do módulo de controle logístico
- [ ] Desenvolvimento do módulo de auditoria de contratos
- [ ] Implementação de autenticação e perfis de acesso
- [ ] Testes automatizados
- [ ] Deploy em ambiente de produção

---

## 👥 Equipe

Projeto desenvolvido por:

| Nome                          |
|-------------------------------|
| Ana Beatriz da Silva           |
| Deivisson da Silva Rocha       |
| Felipe de Almeida Silva        |
| Wendell dos Santos             |

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">Desenvolvido com dedicação para otimizar a logística e a gestão de contratos 🚛📊</p>
