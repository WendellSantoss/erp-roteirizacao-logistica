---
id: HU-008
titulo: Calcular e destacar o atraso de cada OS
modulo: Pendências
epico: EP-A Ingestão e preparação de dados
tela: "Gerenciar Pendências" › colunas Decorrido e Atraso
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-PEN-04]
regras: [RN-06]
nao_funcionais: []
depende_de: [HU-007, HU-066]
---

# HU-008 — Calcular e destacar o atraso de cada OS

## História
Como **Analista de Operações**, quero **ver quanto tempo cada OS já consumiu e quanto passou do
prazo contratual, com destaque para as atrasadas**, para **priorizar as que geram penalidade
para o contrato**.

## Regras de negócio
- **RN-06** — Atraso = (agora − abertura) − prazo contratual em horas. Positivo = em atraso.
- **RN-L01** — Decorrido = agora − abertura.
- **RN-L02** — O prazo é o da coluna "Prazo (h)" da planilha; se vier vazio, usa o prazo
  parametrizado para o tipo de serviço (HU-066).
- **RN-L03** — Faixas: **em atraso** (atraso > 0, vermelho); **vence em até 4 h** (atraso entre
  −4 h e 0, amarelo); **no prazo** (sem destaque).
- **RN-L04** — O cálculo usa o fuso `America/Fortaleza` e é feito no servidor, para todos
  verem o mesmo valor.

## Critérios de aceite
CA01 — Em atraso
Dado agora 11/07/2026 14:00, abertura 10/07/2026 08:00 e prazo 24 h
Quando olho a OS
Então Decorrido "30h 0min", Atraso "6h 0min" em vermelho.

CA02 — Exatamente no limite
Dado abertura 10/07/2026 14:00 e prazo 24 h, agora 11/07/2026 14:00
Quando olho a OS
Então Atraso "0h 0min" e a OS **não** é classificada como atrasada (amarela).

CA03 — No prazo
Dado abertura 11/07/2026 08:00, prazo 48 h e agora 11/07/2026 14:00
Quando olho a OS
Então Decorrido "6h 0min", Atraso "—" e nenhum destaque.

CA04 — Atualização
Dado uma OS que vence às 14:00
Quando a tela fica aberta até 14:01
Então a OS passa a vermelho em até 1 min sem recarregar a página.

CA05 — Prazo vazio
Dado uma OS sem prazo na planilha e o tipo "Religação" parametrizado com 24 h
Quando o atraso é calculado
Então usa 24 h.

## Dúvidas em aberto
- O prazo conta horas corridas ou só o horário operacional (05h–20h, dias úteis)? A fórmula da
  ERS indica horas corridas.
