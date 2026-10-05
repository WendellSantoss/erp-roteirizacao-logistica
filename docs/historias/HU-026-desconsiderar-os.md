---
id: HU-026
titulo: Desconsiderar uma OS
ordem: 34
modulo: Pendências
epico: EP-A Ingestão e preparação de dados
tela: "Gerenciar Pendências" › coluna Desconsiderar
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-PEN-05]
regras: [RN-02, RN-07]
nao_funcionais: [RNF-12, RNF-15]
depende_de: [HU-006, HU-020, HU-F11]
---

# HU-026 — Desconsiderar uma OS

## História
Como **Analista de Operações**, quero **retirar da operação uma OS que não deve ser executada**,
para **que ela não seja roteirizada nem cobrada, sem afetar as demais**.

## Regras de negócio
- **RN-07** — OS desconsiderada não é roteirizada, não entra na produção bruta nem no BM.
- **RN-02** — A desconsideração sobrevive a reimportações.
- **RNF-12** — Ação crítica: só perfis autorizados (Analista de Operações, Gerente de Contrato) e
  sempre registrada.
- **RN-L01** — Exige justificativa de pelo menos 10 caracteres.
- **RN-L02** — Só OSs em "Pendente" ou "Apta a roteirizar". "Desconsiderada" é estado terminal.

## Critérios de aceite
CA01 — Desconsiderar
Dado a OS 4471203 "Pendente"
Quando clico em Desconsiderar, escrevo "OS duplicada no GSAN" e confirmo
Então a OS passa a "Desconsiderada", sai da lista, aparece o toast "OS 4471203 desconsiderada" e
a trilha registra autor, data/hora e justificativa.

CA02 — Confirmação
Dado o diálogo de confirmação aberto
Quando clico em Cancelar
Então nada muda.

CA03 — Sem justificativa
Dado o diálogo com justificativa "erro"
Quando confirmo
Então aparece "Justificativa com pelo menos 10 caracteres" e nada muda.

CA04 — Estado não permitido
Dado uma OS "Roteirizada"
Quando chamo a API de desconsiderar
Então recebo `422` "Só OSs pendentes ou aptas podem ser desconsideradas".

CA05 — Perfil sem permissão
Dado um Coordenador de Campo
Quando chama a API de desconsiderar
Então recebe `403`.

CA06 — Não volta na importação
Dado a OS desconsiderada
Quando ela vem de novo na planilha do dia seguinte
Então continua "Desconsiderada".

## Fora de escopo
Desfazer a desconsideração (não previsto na ERS).
