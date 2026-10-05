---
id: HU-042
titulo: Ver a produção validada e a taxa de conversão
ordem: 58
modulo: Gerencial
epico: EP-D Fechamento, auditoria e faturamento
tela: "Gerencial" › cartão "Produção validada"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-GER-02]
regras: [RN-14, RN-17]
nao_funcionais: [RNF-21]
depende_de: [HU-041]
---

# HU-042 — Ver a produção validada e a taxa de conversão

## História
Como **Gerente de Contrato**, quero **ver quanto da produção foi validado e o percentual de
conversão**, para **medir a qualidade da execução e o que de fato será faturado**.

## Regras de negócio
- **RN-17** — Conversão = produção validada ÷ produção bruta, em %.
- **RN-L01** — Produção validada = OSs em "Validada" ou "Faturada" no período e polo.
- **RN-L02** — Conversão com 1 casa decimal; sem produção bruta, mostra "—".

## Critérios de aceite
CA01 — Cartão
Dado 1.240 OSs na produção bruta e 812 validadas somando R$ 204.624,00
Quando abro o Gerencial
Então o cartão mostra "812", "65,5% de conversão" e "R$ 204.624,00".

CA02 — Sem produção bruta
Dado 0 OSs executadas
Quando abro
Então a conversão mostra "—" (sem divisão por zero).

CA03 — Validação forçada entra
Dado uma OS invalidada que teve a validação forçada (HU-062)
Quando atualizo o Gerencial
Então ela passa a contar na produção validada.
