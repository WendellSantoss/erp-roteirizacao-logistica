---
id: HU-054
titulo: Escolher o polo de trabalho em qualquer tela
modulo: Transversal
epico: EP-F Requisitos transversais
tela: Cabeçalho › seletor "Polo 1 - Central / Polo 2 - Norte / Polo 3 - Sul"
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-TRV-03]
regras: [RN-20]
nao_funcionais: [RNF-26]
depende_de: [HU-020, HU-F11]
---

# HU-054 — Escolher o polo de trabalho em qualquer tela

## História
Como **usuário do GeniOS**, quero **escolher no cabeçalho o polo com que estou trabalhando**,
para **que listas, mapas, saldos e indicadores mostrem só aquele polo**.

## Regras de negócio
- **RN-L01** — Opções: os polos permitidos ao usuário; "Todos" só aparece se ele tem mais de um polo.
- **RN-L02** — Com "Todos": leitura agregada e coluna Polo visível; ações de escrita que
  dependem de polo (importar, criar rota, saída de kit) ficam bloqueadas (ERS §2.3).
- **RN-L03** — A escolha é lembrada entre sessões do mesmo usuário.
- **RN-L04** — O filtro de polo é aplicado no servidor em toda consulta (não só na tela).

## Critérios de aceite
CA01 — Trocar
Dado o Gerente no Polo 1 vendo Pendências
Quando escolhe "Polo 2 - Norte"
Então a lista, os contadores e o cabeçalho passam a mostrar o Polo 2 sem recarregar a página.

CA02 — "Todos"
Dado o Gerente
Quando escolhe "Todos"
Então as listas mostram os 3 polos com coluna Polo, e "Criar Rota" e "Registrar saída" ficam
desabilitados com "Selecione um polo".

CA03 — Polo único
Dado o Almoxarife com acesso só ao Polo 2
Quando abre o sistema
Então o seletor mostra só "Polo 2 - Norte", sem "Todos".

CA04 — Servidor
Dado o Almoxarife do Polo 2
Quando chama a API pedindo dados do Polo 1
Então recebe `403`.

CA05 — Lembrar
Dado que escolhi o Polo 3 e saí
Quando entro de novo
Então o Polo 3 já está selecionado.
