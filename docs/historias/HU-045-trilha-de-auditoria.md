---
id: HU-045
titulo: Manter a trilha de auditoria das alterações
modulo: Transversal
epico: EP-F Requisitos transversais
tela: — (consulta a desenhar)
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-TRV-04]
regras: [RN-13]
nao_funcionais: [RNF-15, RNF-16, RNF-17]
depende_de: [HU-019, HU-F03]
---

# HU-045 — Manter a trilha de auditoria das alterações

## História
Como **Gerente de Contrato**, quero **um registro imutável de toda alteração em dado operacional
ou financeiro**, para **provar, a qualquer momento da vigência do contrato, quem fez o quê**.

## Contexto
É a peça que quase todas as histórias usam ("a trilha registra…"). Por isso vem na fase 1, logo
após a fundação. A HU-040 é o caso particular da grade de auditoria.

## Regras de negócio
- **RNF-15** — Cada registro: autor, data/hora, entidade e id, campo, valor anterior, valor novo,
  origem (tela, importação, assistente) e justificativa quando houver.
- **RNF-16** — Imutável; consultável por OS, usuário e período; retenção mínima de 5 anos (proposta).
- **RN-L01** — Alteração e registro na mesma transação: sem registro, sem alteração.

## Critérios de aceite
CA01 — Registro automático
Dado qualquer alteração em OS, rota, equipe, kit, movimentação, invalidação, BM ou parâmetro
Quando ela é salva
Então existe um registro com os campos de RNF-15.

CA02 — Consulta
Dado o Gerente
Quando consulta a trilha pela OS 4471203
Então vê todos os eventos dela, em ordem, da importação ao faturamento.

CA03 — Por usuário e período
Dado o Gerente
Quando filtra por "Carla" e 01/07 a 15/07
Então vê só as alterações da Carla nesse período.

CA04 — Imutável
Dado qualquer usuário, inclusive Administrador
Quando tenta alterar ou apagar um registro pela API ou pelo painel administrativo
Então a operação não existe ou é recusada.

CA05 — Desempenho
Dado 1.000.000 de registros
Quando consulto por OS
Então o resultado vem em até 2 s.
