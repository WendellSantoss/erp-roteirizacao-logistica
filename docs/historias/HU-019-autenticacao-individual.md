---
id: HU-019
titulo: Entrar no sistema com usuário individual
modulo: Transversal
epico: EP-F Requisitos transversais
tela: Cabeçalho › usuário ("Ana Duarte · Gerente de Contrato"); tela de login a desenhar
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-TRV-01]
regras: []
nao_funcionais: [RNF-11, RNF-13]
depende_de: [HU-F03, HU-F04]
---

# HU-019 — Entrar no sistema com usuário individual

## História
Como **usuário do GeniOS**, quero **entrar com meu próprio usuário e senha e ver meu nome e papel
no cabeçalho**, para **que toda ação fique registrada em meu nome**.

## Regras de negócio
- **RN-L01** — Login por e-mail e senha. Senha com pelo menos 10 caracteres, letras e números (RNF-11, proposta).
- **RN-L02** — 5 tentativas erradas seguidas bloqueiam o usuário por 15 min.
- **RN-L03** — Sessão expira após 30 min sem atividade (RNF-11, proposta).
- **RN-L04** — Usuário desativado não entra.
- **RN-L05** — Mensagem de erro de login não diz se o e-mail existe.

## Critérios de aceite
CA01 — Entrar
Dado a usuária ana@genios.local, ativa, Gerente de Contrato
Quando entra com a senha correta
Então vai para a tela inicial e o cabeçalho mostra "Ana Duarte · Gerente de Contrato" e as iniciais "AD".

CA02 — Senha errada
Dado senha errada ou e-mail inexistente
Quando tento entrar
Então aparece "E-mail ou senha inválidos" nos dois casos.

CA03 — Bloqueio
Dado 5 tentativas erradas seguidas
Quando tento a 6ª, mesmo com a senha certa
Então aparece "Muitas tentativas. Tente novamente em 15 minutos".

CA04 — Inatividade
Dado 30 min sem atividade
Quando clico em qualquer coisa
Então sou levado ao login com "Sessão expirada", e depois de entrar volto à tela onde estava.

CA05 — Sair
Dado o usuário logado
Quando clica em "Sair"
Então a sessão é encerrada e voltar no navegador não mostra dados.

CA06 — Sem login
Dado nenhuma sessão
Quando chamo qualquer endpoint da API (exceto login e saúde)
Então recebo `401`.

## Fora de escopo
Cadastro de usuários (HU-065), recuperação de senha por e-mail (a definir).
