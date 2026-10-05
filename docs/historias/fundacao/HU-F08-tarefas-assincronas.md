---
id: HU-F08
titulo: Executar tarefas assíncronas com progresso
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-05]
depende_de: [HU-F03]
---

# HU-F08 — Executar tarefas assíncronas com progresso

## História
Como **desenvolvedor do GeniOS**, quero **um mecanismo padrão para rodar tarefas longas fora da
requisição e consultar o progresso delas**, para **que importação (HU-001/021) e webscraper
(HU-005/022) não bloqueiem a navegação (RNF-05) e reusem a mesma peça**.

## Critérios de aceite
CA01 — Disparo não bloqueante
Dado uma tarefa de exemplo que dura 30 s
Quando chamo o endpoint que a dispara
Então recebo `202` com o id da tarefa em até 500 ms.

CA02 — Progresso consultável
Dado uma tarefa em execução
Quando consulto `GET /api/tarefas/<id>`
Então recebo estado (`na fila`, `executando`, `concluída`, `falhou`), percentual, etapa atual e
mensagem.

CA03 — Falha registrada
Dado uma tarefa que lança erro
Quando ela termina
Então o estado é `falhou`, a mensagem é legível em pt-BR e o erro técnico vai para o log (RNF-28).

CA04 — Componente de progresso
Dado o frontend
Quando acompanho uma tarefa
Então um componente reutilizável mostra percentual e etapa, atualizando ao menos a cada 2 s, e
continua mostrando o estado certo se eu navegar para outra tela e voltar.
