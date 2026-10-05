---
id: HU-006
titulo: Listar as OSs que precisam de tratamento
modulo: Pendências
epico: EP-A Ingestão e preparação de dados
tela: "Gerenciar Pendências"
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-PEN-01]
regras: [RN-04, RN-07]
nao_funcionais: [RNF-02, RNF-20]
depende_de: [HU-004, HU-054]
---

# HU-006 — Listar as OSs que precisam de tratamento

## História
Como **Analista de Operações**, quero **uma lista das OSs importadas que ainda precisam de
tratamento antes do despacho**, para **saber o que falta resolver para a carteira ficar pronta
para roteirização**.

## Regras de negócio
- **RN-L01** — A lista mostra OSs em "Pendente" do polo selecionado (com "Todos", dos polos do
  usuário e com a coluna Polo visível).
- **RN-L02** — Ordenação padrão: prioritárias primeiro, depois maior atraso.
- **RN-L03** — Paginação de 50 linhas; o total de OSs da lista aparece no topo.

## Critérios de aceite
CA01 — Lista
Dado 312 OSs "Pendente" no Polo 1 e 500 em outros estados
Quando abro Gerenciar Pendências no Polo 1
Então vejo "312 OSs pendentes", a primeira página com 50, ordenadas por prioridade e atraso.

CA02 — Saída da lista
Dado uma OS pendente
Quando ela é tratada (HU-060) ou desconsiderada (HU-026)
Então ela sai da lista sem recarregar a página e o total diminui em 1.

CA03 — Desempenho (RNF-02)
Dado uma carteira de 50.000 OSs no banco
Quando abro a lista
Então a primeira página aparece em até 2 s.

CA04 — Lista vazia (RNF-20)
Dado nenhuma OS pendente
Quando abro a lista
Então vejo "Nenhuma pendência neste filtro" e a orientação de que as OSs seguem para o
Roteirizador ou de importar a planilha do dia.

CA05 — "Todos"
Dado o seletor em "Todos" e um usuário com acesso aos 3 polos
Quando abro a lista
Então vejo as pendências dos 3 polos com a coluna Polo.

CA06 — Ver detalhes
Dado uma OS na lista
Quando clico nela
Então vejo todos os dados da OS, inclusive o histórico de importações que a atualizaram.
