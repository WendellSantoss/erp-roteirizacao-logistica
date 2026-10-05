---
id: HU-049
titulo: Abrir o assistente de qualquer tela
ordem: 77
modulo: Assistente
epico: EP-E Inteligência e suporte à decisão
tela: "Assistente GeniOS" (painel lateral, "● online · NLP integrado")
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ASS-01]
regras: [RN-20]
nao_funcionais: [RNF-13, RNF-14]
depende_de: [HU-019, HU-F04]
---

# HU-049 — Abrir o assistente de qualquer tela

## História
Como **usuário do GeniOS (qualquer perfil)**, quero **abrir o assistente em qualquer tela e saber
se ele está disponível**, para **perguntar algo no meio do trabalho sem sair de onde estou**.

## Regras de negócio
- **RN-L01** — Online = o serviço de linguagem respondeu a uma verificação nos últimos 60 s.
- **RN-L02** — A conversa da sessão é mantida ao trocar de tela; ao sair do sistema, é apagada da tela.
- **RN-L03** — As conversas são registradas no servidor (pergunta, resposta, usuário, data/hora)
  por 90 dias, para auditoria e melhoria (proposta).

## Critérios de aceite
CA01 — Abrir
Dado qualquer tela do sistema
Quando clico no botão do assistente
Então o painel abre sem sair da tela atual, com o indicador "● online".

CA02 — Offline
Dado o serviço de linguagem indisponível
Quando abro o painel
Então o indicador mostra "● offline", o campo de mensagem fica desabilitado com "Assistente
indisponível no momento", e o resto do sistema funciona normalmente.

CA03 — Conversa mantida
Dado uma conversa com 3 mensagens
Quando navego de Pendências para Gerencial
Então as 3 mensagens continuam no painel.

CA04 — Fechar
Dado o painel aberto
Quando clico em ✕ ou pressiono Esc
Então o painel fecha.
