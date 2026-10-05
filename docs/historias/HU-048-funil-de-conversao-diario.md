---
id: HU-048
titulo: Ver o funil de conversão diário
modulo: Gerencial
epico: EP-D Fechamento, auditoria e faturamento
tela: "Gerencial" › "Funil de conversão diário"
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-GER-05]
regras: [RN-07]
nao_funcionais: [RNF-02]
depende_de: [HU-041, HU-F11]
---

# HU-048 — Ver o funil de conversão diário

## História
Como **Gerente de Contrato**, quero **ver, para um dia, quantas OSs passaram por cada etapa do
ciclo de vida e onde elas se perdem**, para **atacar o gargalo certo (tratamento, despacho,
execução ou fiscalização)**.

## Regras de negócio
- **RN-L01** — Etapas: Importadas → Aptas → Roteirizadas → Despachadas → Executadas → Validadas.
- **RN-L02** — Para cada etapa: quantidade e perda em relação à etapa anterior (quantidade e %).
- **RN-L03** — Desconsideradas aparecem como perda entre Importadas e Aptas, identificadas.

## Critérios de aceite
CA01 — Funil
Dado 11/07 no Polo 1 com 1.240 importadas, 1.100 aptas, 950 roteirizadas, 950 despachadas,
880 executadas e 812 validadas
Quando abro o funil
Então vejo as 6 etapas com essas quantidades e a perda de cada passo (ex.: "Executadas → Validadas: −68 (−7,7%)").

CA02 — Escolher o dia
Dado o funil
Quando escolho outro dia
Então os números são recalculados para ele.

CA03 — Desconsideradas
Dado 40 OSs desconsideradas no dia
Quando abro o funil
Então a perda entre Importadas e Aptas mostra quanto é desconsideração.

## Dúvidas em aberto
- A ERS marca este requisito como Obrigatório; a issue original tinha prioridade Baixa. Mantido como MVP.
