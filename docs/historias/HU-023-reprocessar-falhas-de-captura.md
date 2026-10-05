---
id: HU-023
titulo: Ver e reprocessar as unidades cuja captura falhou
modulo: Webscraper
epico: EP-A Ingestão e preparação de dados
tela: — (sem tela no protótipo; acessada pelo indicador do cabeçalho)
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-WEB-03]
regras: [RN-04]
nao_funcionais: [RNF-19]
depende_de: [HU-005, HU-022]
---

# HU-023 — Ver e reprocessar as unidades cuja captura falhou

## História
Como **Analista de Operações**, quero **ver quais unidades não tiveram coordenada capturada e
mandar capturar de novo só as que eu escolher**, para **resolver as falhas sem refazer a
captura inteira**.

## Critérios de aceite
CA01 — Lista de falhas
Dado 4 unidades com falha de captura no Polo 1
Quando abro a lista de falhas
Então vejo, para cada unidade: código, nome, quantidade de OSs afetadas, motivo da falha, data
da última tentativa e número de tentativas.

CA02 — Reprocessar selecionadas
Dado a lista com 4 falhas
Quando seleciono 2 e clico em "Capturar novamente"
Então apenas essas 2 são capturadas de novo; as que derem certo saem da lista.

CA03 — Ordem por impacto
Dado a lista de falhas
Quando abro
Então ela está ordenada pela quantidade de OSs afetadas, da maior para a menor.

CA04 — Saída para preenchimento manual
Dado uma unidade com 3 tentativas falhas
Quando olho a linha
Então há a ação "Informar coordenada" que abre o preenchimento manual (HU-024).
