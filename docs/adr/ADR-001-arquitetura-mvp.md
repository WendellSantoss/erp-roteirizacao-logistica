# ADR-001 — Escolha da arquitetura do MVP do GeniOS

* **Status:** Aceita
* **Data da decisão:** 06/10/2026
* **Decisores:** Ana Beatriz da Silva, Deivisson da Silva Rocha, Felipe de Almeida Silva e Wendell dos Santos (equipe do projeto)
* **Decisão:** Monólito Modular com Processamento Assíncrono
* **Sistema:** GeniOS — Sistema ERP Operacional para Roteirização, Controle Logístico e Auditoria de Contratos

---

## 1. Contexto — Qual problema motivou a decisão

O grupo precisava escolher uma arquitetura para o MVP do GeniOS considerando o prazo de desenvolvimento, o tamanho da equipe, o volume de dados previsto e os principais atributos de qualidade identificados.

A análise das histórias de usuário e dos requisitos não funcionais mostrou que os atributos que mais pressionam a arquitetura são integridade e confiabilidade dos dados, segurança das regras de negócio e auditabilidade/rastreabilidade.

O sistema possui operações críticas, como importação e atualização de OSs sem perda de tratamentos, controle de saída de kits, registro das alterações de auditoria, geração de arquivos RPA e integração com sistemas externos. Portanto, a arquitetura precisava garantir consistência e segurança sem acrescentar uma complexidade maior do que a necessária para o MVP.

---

## 2. Decisão — O que foi escolhido

O grupo escolheu utilizar uma arquitetura de **Monólito Modular com Processamento Assíncrono** para o MVP do GeniOS.

A aplicação será desenvolvida como um único sistema, organizado internamente em módulos de negócio, como:
* Importação e Preparação
* Planejamento e Roteirização
* Suprimentos e Logística
* Auditoria e Fechamento
* Gerencial
* Integrações
* Assistente

As regras de negócio críticas serão executadas no servidor, garantindo a integridade dos dados, a aplicação das regras de segurança e o registro das operações que precisam de rastreabilidade.

O processamento assíncrono será utilizado para tarefas demoradas, como importações e captura de coordenadas, evitando que essas operações bloqueiem a utilização do sistema.

A escolha foi feita pelo grupo por apresentar o melhor equilíbrio entre os atributos de qualidade prioritários, a complexidade da solução, o prazo e a capacidade da equipe.

---

## 3. Alternativas — O que mais foi avaliado e por que foi descartado

Foram avaliadas duas propostas de arquitetura geradas com apoio de IA:

1. **Monólito Modular com Processamento Assíncrono — Escolhido**
   Foi considerado adequado para o MVP por facilitar o controle transacional das operações críticas, especialmente a importação e atualização das OSs, a aplicação centralizada das regras de negócio e a implementação da auditabilidade. Também apresenta menor complexidade de desenvolvimento e implantação, sendo mais compatível com o tamanho da equipe e o prazo disponível.

2. **Microsserviços Orientados a Domínios — Descartado**
   A arquitetura de microsserviços foi avaliada por oferecer maior possibilidade de escalabilidade independente, isolamento de falhas e evolução dos serviços. Entretanto, foi descartada para o MVP porque introduziria maior complexidade de desenvolvimento, comunicação entre serviços, monitoramento, tratamento de falhas distribuídas e manutenção da consistência dos dados. Como a escalabilidade não está entre os atributos de maior pressão no MVP, o grupo considerou que os benefícios dos microsserviços não compensam sua complexidade neste momento.

---

## 4. Consequências — Ganhos obtidos e custos aceitos

### Ganhos obtidos
* Maior facilidade para garantir a integridade e consistência dos dados.
* Maior controle das regras de negócio no servidor.
* Facilitação da auditabilidade e rastreabilidade das operações.
* Menor complexidade de desenvolvimento e implantação.
* Menor custo inicial de infraestrutura.
* Melhor adequação ao prazo e ao tamanho da equipe.
* Possibilidade de utilizar processamento assíncrono em operações demoradas.
* Organização interna por módulos, facilitando a manutenção do sistema.

### Custos aceitos
* Os módulos não poderão ser escalados de forma totalmente independente.
* Uma falha grave na aplicação pode afetar mais de um módulo.
* O banco de dados compartilhado pode aumentar o acoplamento entre os módulos.
* O crescimento do sistema exige disciplina para evitar que os módulos fiquem excessivamente acoplados.
* Caso futuramente seja necessária uma arquitetura distribuída, alguns módulos poderão precisar ser refatorados e separados.

Os custos foram considerados aceitáveis pelo grupo porque atendem às necessidades atuais do MVP e permitem entregar uma solução com foco nos atributos considerados mais críticos: integridade, segurança e auditabilidade.

---

## 5. Stack Tecnológica Adotada (Premissas do Projeto Arquitetural)

| Parte do sistema | Tecnologia | Justificativa / Requisito atendido |
| :--- | :--- | :--- |
| **Backend** | Python, Django + Django REST Framework | `transaction.atomic` garante importação transacional (`RNF-07`); um app Django por módulo materializa o monólito modular (`HU-003`). |
| **Tarefas assíncronas** | Celery + Redis | Importação e webscraper rodam fora da requisição, com progresso consultável (`RNF-05`, `HU-008`). |
| **Banco de dados** | PostgreSQL + PostGIS | Transações ACID, seleção por polígono (`RNF-03`) e trigger imutável na auditoria (`RNF-16`). |
| **Frontend** | React + TypeScript, MapLibre GL | Mapa em WebGL para até 2.000 pins (`RNF-03`); cliente tipado gerado do contrato (`HU-F05`). |
| **Captura de coordenadas** | Playwright (headless) | Portal GSAN não oferece API (`PR-03`). |
| **Implantação (MVP)** | Neon (PostgreSQL), Render (Backend) e Vercel (Frontend) | Ambiente publicado em nuvem conforme diretrizes do protótipo implantado. |