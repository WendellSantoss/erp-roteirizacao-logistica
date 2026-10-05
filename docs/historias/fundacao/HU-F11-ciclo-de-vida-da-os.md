---
id: HU-F11
titulo: Modelar as entidades centrais e o ciclo de vida da OS
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: [RN-07, RN-08, RN-10, RN-14, RN-19]
nao_funcionais: [RNF-15, RNF-26]
depende_de: [HU-F03]
---

# HU-F11 — Modelar as entidades centrais e o ciclo de vida da OS

## História
Como **desenvolvedor do GeniOS**, quero **um único ponto do código que define os estados da OS e
as transições permitidas entre eles**, para **que nenhuma história (nem o assistente) consiga
levar uma OS a um estado inválido, e todas mudem o estado do mesmo jeito**.

## Contexto
A ERS (§2.4) diz que o estado da OS é "o eixo que integra os macro-processos" e "a principal
fonte de regras de negócio". Sem uma máquina de estados central, cada história implementaria a
sua própria transição. Esta história cria também as entidades das quais todas dependem: Polo,
Unidade e Ordem de Serviço (ERS §4).

## Regras de negócio
Transições permitidas (qualquer outra é recusada):

| De | Para | Disparada por |
|---|---|---|
| — | Pendente | Upsert de OS nova (HU-004) |
| Pendente | Apta a roteirizar | Conclusão do tratamento (HU-060) |
| Pendente, Apta a roteirizar | Desconsiderada | Desconsiderar (HU-026) |
| Apta a roteirizar | Roteirizada | Criar rota / atribuir despacho (HU-056, HU-057) |
| Roteirizada | Apta a roteirizar | Retirar OS da rota antes do despacho (HU-059) |
| Roteirizada | Despachada | Geração do RPA (HU-014) |
| Despachada | Executada | Conciliação da execução (HU-018) |
| Despachada, Executada | Invalidada | Reprovação da fiscalização (HU-018) |
| Executada | Validada | Aprovação na auditoria (HU-039) |
| Invalidada | Validada | Forçar validação (HU-062) |
| Validada | Faturada | Fechamento do ciclo (HU-064) |
| Faturada | Validada | Reabertura do ciclo (HU-064) |

> O estado "Importada" da ERS é transitório: a OS nova termina o upsert já em "Pendente".

- **RN-L01** — Desconsiderada é terminal (RN-07). Faturada só sai por reabertura de ciclo.
- **RN-L02** — Polo e Unidade são cadastros; incluir um polo novo não exige alteração de
  código nem de estrutura do banco (RNF-26).

## Critérios de aceite
CA01 — Transição permitida
Dado uma OS em "Pendente"
Quando o serviço de transição a leva para "Apta a roteirizar"
Então o estado muda e é registrado na trilha com autor, data/hora, estado anterior e novo.

CA02 — Transição proibida
Dado uma OS em "Desconsiderada"
Quando qualquer código tenta levá-la para "Roteirizada"
Então a operação é recusada com erro de domínio "Transição não permitida: Desconsiderada →
Roteirizada" e nada muda.

CA03 — Tabela completa testada
Dado a tabela de transições acima
Quando os testes rodam
Então existe um teste para cada transição permitida e um teste garantindo que todas as demais
combinações de estado são recusadas.

CA04 — Estado só muda pelo serviço
Dado o código do backend
Quando procuro atribuições diretas ao campo de estado fora do serviço de transição
Então não encontro (verificado por teste ou regra de lint).

CA05 — Novo polo sem código
Dado o cadastro de polos
Quando o Administrador inclui "Polo 4 – Oeste"
Então ele aparece no seletor de polo sem nova versão do sistema.

## Fora de escopo
As telas que disparam cada transição (histórias citadas na tabela).
