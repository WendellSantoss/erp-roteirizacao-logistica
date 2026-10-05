---
id: HU-022
titulo: Ver o progresso da captura no cabeçalho
ordem: 30
modulo: Webscraper
epico: EP-A Ingestão e preparação de dados
tela: Cabeçalho › "Webscraper — Capturando coords. 77 / 120 unidades"
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-WEB-02]
regras: []
nao_funcionais: [RNF-05]
depende_de: [HU-005]
---

# HU-022 — Ver o progresso da captura no cabeçalho

## História
Como **Analista de Operações**, quero **ver no cabeçalho, de qualquer tela, quantas unidades já
foram capturadas**, para **saber quando o mapa estará completo sem precisar abrir outra página**.

## Critérios de aceite
CA01 — Indicador
Dado uma captura em andamento com 77 de 120 unidades processadas
Quando olho o cabeçalho em qualquer tela
Então vejo "Capturando coords. 77 / 120 unidades", atualizado ao menos a cada 5 s.

CA02 — Fim da captura
Dado a captura concluída com 4 falhas
Quando a última unidade é processada
Então o indicador mostra "Coordenadas: 116 / 120 · 4 falhas" e um clique leva à lista de falhas (HU-023).

CA03 — Sem captura
Dado nenhuma captura em andamento e nenhuma falha pendente
Quando olho o cabeçalho
Então o indicador não aparece.

CA04 — Polo
Dado o seletor de polo no Polo 2
Quando há captura em andamento para o Polo 1
Então o indicador não mostra a captura do Polo 1; com "Todos", soma as capturas dos polos.
