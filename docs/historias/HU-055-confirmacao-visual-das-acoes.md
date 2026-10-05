---
id: HU-055
titulo: Ver a confirmação de cada ação concluída
ordem: 21
modulo: Transversal
epico: EP-F Requisitos transversais
tela: Toast ("✓ mensagem") em todas as telas
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-TRV-05]
regras: []
nao_funcionais: [RNF-19, RNF-22]
depende_de: [HU-F04]
---

# HU-055 — Ver a confirmação de cada ação concluída

## História
Como **usuário do GeniOS**, quero **um aviso discreto quando uma ação dá certo**, para **ter
certeza de que foi feito sem precisar conferir em outra tela**.

## Regras de negócio
- **RN-L01** — Sucesso: toast verde com ✓, some sozinho em 5 s, não bloqueia a tela.
- **RN-L02** — Erro: mensagem no lugar do erro (campo, diálogo) quando houver; toast de erro
  só para falhas gerais, e ele fica até o usuário fechar.
- **RN-L03** — Texto diz o que aconteceu com o objeto: "Rota Bessa manhã criada com 18 OSs", não "Sucesso".
- **RN-L04** — Vários toasts se empilham; no máximo 3 visíveis.

## Critérios de aceite
CA01 — Sucesso
Dado qualquer ação concluída (salvar equipe, criar rota, registrar saída…)
Quando ela termina
Então aparece o toast com a mensagem específica e ele some após 5 s, sem impedir cliques.

CA02 — Erro geral
Dado uma falha de rede
Quando a ação falha
Então aparece um toast de erro que fica até eu fechar.

CA03 — Acessível
Dado um leitor de tela
Quando um toast aparece
Então ele é anunciado (região `aria-live`).
