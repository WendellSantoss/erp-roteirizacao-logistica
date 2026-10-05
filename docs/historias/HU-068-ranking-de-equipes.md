---
id: HU-068
titulo: Ver o ranking de equipes
modulo: Gerencial
epico: EP-D Fechamento, auditoria e faturamento
tela: "Gerencial" › "Ranking de equipes"
fase: 3
prioridade: desejável
status: proposta
requisitos: [RF-GER-06 (proposto)]
regras: []
nao_funcionais: []
depende_de: [HU-042]
---

# HU-068 — Ver o ranking de equipes

> **Proposta — validar com o grupo.** Aparece no protótipo mas não está na ERS. Marcada como
> desejável, fora do MVP, até o grupo decidir.

## História
Como **Gerente de Contrato**, quero **ver as equipes ordenadas pela produção validada**, para
**reconhecer as melhores e acompanhar as que mais têm reprovação**.

## Critérios de aceite
CA01 — Ranking
Dado o período e o polo selecionados
Quando abro o ranking
Então as equipes aparecem ordenadas por valor validado, com posição, nome, valor e taxa de conversão.

CA02 — Empate
Dado duas equipes com o mesmo valor validado
Quando o ranking é montado
Então desempata pela maior taxa de conversão.
