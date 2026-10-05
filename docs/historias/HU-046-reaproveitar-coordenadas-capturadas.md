---
id: HU-046
titulo: Reaproveitar coordenadas já capturadas
ordem: 35
modulo: Webscraper
epico: EP-A Ingestão e preparação de dados
tela: —
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-WEB-05]
regras: [RN-05]
nao_funcionais: [RNF-01]
depende_de: [HU-005]
---

# HU-046 — Reaproveitar coordenadas já capturadas

## História
Como **Analista de Operações**, quero **que unidades que já têm coordenada não sejam capturadas
de novo a cada importação**, para **que a captura diária termine rápido e não sobrecarregue o
portal do GSAN (RN-05)**.

## Regras de negócio
- **RN-L01** — A coordenada pertence à **unidade**, não à OS: OSs novas de uma unidade já
  geolocalizada recebem a coordenada na hora, sem captura.
- **RN-L02** — Unidade com coordenada válida só é capturada de novo por ação manual "Atualizar
  coordenada".

## Critérios de aceite
CA01 — Sem recaptura
Dado 120 unidades na planilha, 110 já com coordenada válida
Quando a importação termina
Então a captura processa só as 10 sem coordenada e o indicador mostra "0 / 10".

CA02 — OS nova herda
Dado a unidade "Manaíra" com coordenada
Quando chega uma OS nova dela
Então a OS aparece no mapa logo após a importação, sem esperar captura.

CA03 — Atualização forçada
Dado uma unidade com coordenada capturada
Quando o Analista clica "Atualizar coordenada"
Então só essa unidade é capturada de novo.

## Dúvidas em aberto
- O que faz uma unidade "mudar" (ERS: "unidades inalteradas")? Se o GSAN altera endereço da
  unidade, precisamos de um campo que indique isso.
