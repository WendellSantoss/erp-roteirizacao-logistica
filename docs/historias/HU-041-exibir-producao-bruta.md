---
id: HU-041
titulo: Ver a produção bruta do período
ordem: 57
modulo: Gerencial
epico: EP-D Fechamento, auditoria e faturamento
tela: "Gerencial" › cartão "Produção bruta"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-GER-01]
regras: [RN-07, RN-16]
nao_funcionais: [RNF-02, RNF-21]
depende_de: [HU-018, HU-054]
---

# HU-041 — Ver a produção bruta do período

## História
Como **Gerente de Contrato**, quero **ver quantas OSs foram executadas no período e quanto isso
vale em reais**, para **saber o teto do que o contrato pode faturar**.

## Regras de negócio
- **RN-L01** — Produção bruta = OSs com execução no período, em qualquer estado a partir de
  "Executada" (Executada, Invalidada, Validada, Faturada). Desconsideradas nunca entram (RN-07).
- **RN-L02** — Valor = soma do valor de cada OS (RN-16).
- **RN-L03** — Filtros: período (padrão: ciclo vigente) e polo (seletor global).

## Critérios de aceite
CA01 — Cartão
Dado 1.240 OSs executadas no ciclo de julho no Polo 1, somando R$ 312.480,00
Quando abro o Gerencial
Então o cartão mostra "1.240 OSs executadas" e "R$ 312.480,00".

CA02 — Polo
Dado o seletor em "Todos"
Quando abro o Gerencial
Então o cartão soma os polos do usuário.

CA03 — Período
Dado o filtro de período 01/07 a 15/07
Quando aplico
Então o cartão considera só execuções nessas datas.

CA04 — Sem dados
Dado um período sem execução
Quando aplico
Então o cartão mostra "0 OSs" e "R$ 0,00".
