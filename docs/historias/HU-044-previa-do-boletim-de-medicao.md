---
id: HU-044
titulo: Ver a prévia do Boletim de Medição do polo
ordem: 60
modulo: Gerencial
epico: EP-D Fechamento, auditoria e faturamento
tela: "Gerencial" › cartão "Prévia BM"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-GER-04]
regras: [RN-16, RN-19]
nao_funcionais: [RNF-21, RNF-25]
depende_de: [HU-042]
---

# HU-044 — Ver a prévia do Boletim de Medição do polo

## História
Como **Gerente de Contrato**, quero **ver quanto o polo tem a faturar no ciclo, detalhado por
item**, para **antecipar o faturamento e conferir antes do fechamento**.

## Regras de negócio
- **RN-19** — Só OSs "Validada" do ciclo vigente.
- **RN-L01** — Item do BM = tipo de serviço: quantidade × preço unitário vigente = subtotal.

## Critérios de aceite
CA01 — Prévia
Dado o ciclo de julho do Polo 1 com 812 OSs validadas
Quando abro a prévia do BM
Então vejo cada tipo de serviço com quantidade, preço unitário e subtotal, e o total "R$ 204.624,00 a faturar no ciclo".

CA02 — Por polo
Dado o seletor em "Todos"
Quando abro a prévia
Então vejo um total por polo e o total geral.

CA03 — Exportar
Dado a prévia
Quando clico em "Exportar"
Então baixo o BM em `.xlsx` e `.pdf` com os mesmos números (RNF-25).

CA04 — Só validadas
Dado uma OS "Executada" ainda não validada
Quando abro a prévia
Então ela não aparece.
