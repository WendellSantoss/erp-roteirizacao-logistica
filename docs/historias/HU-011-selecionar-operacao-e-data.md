---
id: HU-011
titulo: Escolher a operação e a data do planejamento
ordem: 37
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › Operação e Data da Rota
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-ROT-01]
regras: [RN-08]
nao_funcionais: []
depende_de: [HU-054, HU-066]
---

# HU-011 — Escolher a operação e a data do planejamento

## História
Como **Coordenador de Campo**, quero **escolher a operação (PSS, XPT Express, Litoral) e a data
que estou planejando**, para **ver no mapa só as OSs e rotas daquele planejamento**.

## Regras de negócio
- **RN-L01** — As operações vêm do cadastro (HU-066).
- **RN-L02** — A data padrão é amanhã; não é permitido escolher data anterior a hoje para planejar
  (datas passadas abrem em modo consulta).
- **RN-L03** — Toda rota pertence a uma operação, uma data e um polo.

## Critérios de aceite
CA01 — Escolher
Dado o Polo 1
Quando escolho "PSS" e 12/07/2026
Então o mapa e a lista mostram as OSs aptas e as rotas já criadas da PSS para 12/07, e o
cabeçalho do roteirizador mostra "PSS · 12/07/2026".

CA02 — Data passada
Dado que escolho 10/07/2026 (ontem)
Quando a tela abre
Então as rotas daquele dia aparecem só para consulta e "Criar Rota" fica desabilitado com
"Planejamento de data passada é somente leitura".

CA03 — Sem operação
Dado nenhuma operação escolhida
Quando tento criar rota
Então aparece "Escolha a operação".

CA04 — Lembrar escolha
Dado PSS e 12/07 escolhidos
Quando saio e volto ao Roteirizador na mesma sessão
Então a escolha continua.

## Dúvidas em aberto
- O que diferencia as operações (PSS, XPT Express, Litoral)? Tipos de serviço diferentes,
  contratos diferentes ou regiões diferentes? Isso define se a OS "pertence" a uma operação.
