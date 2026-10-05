---
id: HU-014
titulo: Gerar o arquivo de despacho para o RPA
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › "Gerar arquivo RPA"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-ROT-17]
regras: [RN-10]
nao_funcionais: [RNF-17, RNF-25]
depende_de: [HU-013, HU-F11]
---

# HU-014 — Gerar o arquivo de despacho para o RPA

## História
Como **Coordenador de Campo**, quero **gerar o arquivo de despacho das rotas finalizadas no
layout da automação**, para **que o despacho chegue ao sistema da concessionária sem digitação**.

## Regras de negócio
- **RN-10** — Gerar o RPA leva as OSs a "Despachada" e bloqueia novas edições de atribuição.
- **RNF-17** — Cada arquivo é rastreável até o conjunto exato de OSs que o compôs.
- **RN-L01** — Um arquivo por planejamento finalizado (polo + operação + data).
- **RN-L02** — Depois de gerado, o mesmo arquivo pode ser baixado de novo; não é gerado outro.
- **RN-L03** — Geração é tudo ou nada: se falhar, nenhuma OS muda de estado.

## Critérios de aceite
CA01 — Gerar
Dado o planejamento Polo 1 · PSS · 12/07 finalizado com 92 OSs
Quando clico em "Gerar arquivo RPA"
Então um arquivo no layout do RPA é baixado, as 92 OSs passam a "Despachada", e o toast diz
"Arquivo RPA gerado com 92 OSs".

CA02 — Planejamento não finalizado
Dado um planejamento em aberto
Quando tento gerar (tela ou API)
Então o botão está desabilitado e a API responde `422` "Finalize o planejamento antes de gerar o RPA".

CA03 — Rastreabilidade (RNF-17)
Dado o arquivo gerado
Quando consulto o histórico de despachos
Então vejo autor, data/hora, nome do arquivo, um código de verificação (hash) do conteúdo e a
lista das 92 OSs que o compõem.

CA04 — Baixar de novo
Dado o arquivo já gerado
Quando clico em "Baixar novamente"
Então recebo o mesmo arquivo (mesmo hash) e nenhuma OS muda.

CA05 — Edição bloqueada (RN-10)
Dado uma OS despachada
Quando tento trocar a equipe dela
Então a ação é recusada com "OS já despachada".

CA06 — Layout
Dado o arquivo gerado
Quando o comparo com o exemplo de layout fornecido pela automação
Então colunas, ordem, separador e codificação são idênticos (teste automatizado com arquivo de referência).

## Dúvidas em aberto
- **Bloqueante:** precisamos do layout do arquivo RPA (formato, colunas, separador, codificação)
  e de um arquivo de exemplo aceito pela automação.
