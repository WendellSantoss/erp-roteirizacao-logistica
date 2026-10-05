---
id: HU-051
titulo: Receber respostas estruturadas, como o detalhe do BM
ordem: 79
modulo: Assistente
epico: EP-E Inteligência e suporte à decisão
tela: "Assistente GeniOS" › cartão de BM ("Total BM")
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ASS-03]
regras: [RN-19, RN-20]
nao_funcionais: [RNF-21]
depende_de: [HU-050, HU-044]
---

# HU-051 — Receber respostas estruturadas, como o detalhe do BM

## História
Como **Gerente de Contrato**, quero **que respostas com vários números venham organizadas em
tabela ou cartão**, para **ler o BM ou um ranking na conversa sem confusão**.

## Critérios de aceite
CA01 — BM
Dado o ciclo de julho do Polo 1
Quando pergunto "me mostra o BM do polo central"
Então a resposta traz um cartão com título do BM, uma linha por item (tipo de serviço e valor) e
"Total BM" igual ao da prévia (HU-044).

CA02 — Lista
Dado a pergunta "quais as 5 OSs mais atrasadas?"
Quando envio
Então a resposta traz uma tabela com número, unidade e atraso, e link para cada OS.

CA03 — Formatos
Dado qualquer resposta com valores
Quando exibida
Então moeda, datas e números seguem o formato brasileiro.
