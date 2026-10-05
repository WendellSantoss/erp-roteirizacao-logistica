---
id: HU-007
titulo: Exibir as colunas operacionais da OS na lista de pendências
ordem: 28
modulo: Pendências
epico: EP-A Ingestão e preparação de dados
tela: "Gerenciar Pendências" › tabela
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-PEN-03]
regras: []
nao_funcionais: [RNF-21, RNF-24]
depende_de: [HU-006]
---

# HU-007 — Exibir as colunas operacionais da OS na lista de pendências

## História
Como **Analista de Operações**, quero **ver na lista todas as colunas de que preciso para decidir
o tratamento**, para **não abrir OS por OS**.

## Regras de negócio
- **RN-L01** — Colunas, nesta ordem: Ordem de Serviço, Especificação, Tipo, Nº do Imóvel, Data
  de Geração, Unidade Atual, Cidade, Setor, Quadra, Longitude, Latitude, Prazo (h), Abertura,
  Decorrido, Atraso, Tipo/Equipe, Prioridade, PP e a ação Desconsiderar.
- **RN-L02** — Datas `dd/mm/aaaa hh:mm`; coordenadas com 4 casas e vírgula; Decorrido e Atraso
  em `Xh Ymin` (RNF-21).
- **RN-L03** — Coordenada ausente aparece como "—" com destaque.

## Critérios de aceite
CA01 — Colunas
Dado uma OS pendente
Quando olho a linha
Então as 18 colunas de RN-L01 aparecem na ordem definida, com os valores gravados para a OS.

CA02 — Formatos
Dado abertura em 2026-07-11 08:05 e latitude −7.08321
Quando olho a linha
Então vejo "11/07/2026 08:05" e "-7,0832".

CA03 — Sem coordenada
Dado uma OS cuja unidade não tem coordenada
Quando olho a linha
Então Latitude e Longitude mostram "—" destacados.

CA04 — Tela pequena (RNF-24)
Dado a janela em 1366×768
Quando a tabela não cabe
Então ela rola horizontalmente dentro do seu contêiner, com a coluna Ordem de Serviço fixa à esquerda.

CA05 — Ordenar por coluna
Dado a lista
Quando clico no cabeçalho "Atraso"
Então a lista inteira (não só a página) é ordenada por atraso.

## Dúvidas em aberto
- O que significa "PP" na prática (pré-programação)? Quem preenche e quais valores assume?
