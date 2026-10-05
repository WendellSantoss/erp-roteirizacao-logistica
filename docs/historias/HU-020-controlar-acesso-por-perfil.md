---
id: HU-020
titulo: Restringir módulos e ações pelo perfil do usuário
modulo: Transversal
epico: EP-F Requisitos transversais
tela: Menu lateral (itens visíveis conforme perfil)
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-TRV-02]
regras: [RN-20]
nao_funcionais: [RNF-12]
depende_de: [HU-019]
---

# HU-020 — Restringir módulos e ações pelo perfil do usuário

## História
Como **Administrador**, quero **que cada perfil veja e faça só o que lhe cabe**, para **que ações
críticas fiquem com quem tem responsabilidade por elas**.

## Regras de negócio
Matriz de acesso (V = vê; E = edita; — = sem acesso). *Proposta derivada da ERS §2.2.*

| Módulo / ação | Gerente | Coordenador | Analista | Almoxarife | Auditor | Admin |
|---|---|---|---|---|---|---|
| Importação, Webscraper | V | V | E | — | — | E |
| Pendências (tratar, desconsiderar) | E | V | E | — | — | V |
| Equipes, profissionais | V | V | — | — | — | E |
| Roteirizador, RPA | V | E | V | — | — | V |
| Almoxarifado | V | V | — | E | — | V |
| Liberar trava | E | — | — | — | — | — |
| Auditoria (grade) | V | — | — | — | E | V |
| Forçar validação, fechar/reabrir ciclo | E | — | — | — | — | — |
| Gerencial | V | V | — | — | V | V |
| Usuários e parâmetros | — | — | — | — | — | E |
| Assistente | V | V | V | V | V | V |

- **RN-L01** — A regra vale no servidor; esconder o botão é só conveniência.
- **RN-L02** — Além do perfil, o usuário tem uma lista de polos permitidos (HU-065); o Gerente tem todos.

## Critérios de aceite
CA01 — Menu
Dado um Almoxarife
Quando entra
Então o menu mostra só Almoxarifado e o Assistente.

CA02 — API
Dado o Almoxarife
Quando chama a API de gerar RPA
Então recebe `403`.

CA03 — Matriz testada
Dado a matriz acima
Quando os testes rodam
Então há teste automatizado para cada célula "—" e para cada ação crítica, verificando `403`.

CA04 — Acesso por URL
Dado o Almoxarife
Quando digita a URL da tela de Auditoria
Então vê "Você não tem acesso a esta área".
