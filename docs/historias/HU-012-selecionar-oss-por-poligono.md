---
id: HU-012
titulo: Selecionar OSs por polígono no mapa
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-ROT-07]
regras: [RN-04, RN-08]
nao_funcionais: [RNF-03]
depende_de: [HU-005, HU-011, HU-060]
---

# HU-012 — Selecionar OSs por polígono no mapa

## História
Como **Coordenador de Campo**, quero **desenhar um polígono no mapa e ter selecionadas todas as
OSs aptas dentro dele**, para **montar uma rota por região de uma vez, em vez de clicar OS por OS**.

## Contexto
No Roteirizador, depois de escolher operação e data (HU-011), o mapa mostra as OSs como pins.
A seleção alimenta o contador (HU-031), a criação de rota (HU-056) e a atribuição de despacho
(HU-057). É a tela com maior exigência de desempenho do sistema (RNF-03).

## Regras de negócio
- **RN-04** e **RN-08** — só aparecem no mapa e só podem ser selecionadas OSs "Apta a
  roteirizar", com coordenada válida e não desconsideradas.
- **RN-L01** — OS exatamente sobre a borda do polígono conta como dentro.
- **RN-L02** — Um novo polígono **soma** à seleção atual; OSs já selecionadas não duplicam.
- **RN-L03** — O mapa mostra só OSs do polo selecionado; com "Todos", o desenho de polígono fica
  desabilitado (criação de rota exige polo, ERS §2.3).

## Critérios de aceite
CA01 — Seleção por polígono (caminho feliz)
Dado o Polo 2 – Norte, a operação PSS e 300 OSs aptas no mapa
Quando desenho um polígono que contém 42 delas
Então exatamente essas 42 ficam destacadas como selecionadas e o contador mostra "42 OSs
selecionadas".

CA02 — Fora do polígono
Dado o CA01
Quando confiro as OSs fora do polígono
Então nenhuma delas está selecionada.

CA03 — OS inapta não aparece
Dado uma OS "Pendente", uma "Desconsiderada" e uma "Apta" sem coordenada, todas na região
Quando desenho um polígono que cobre a região
Então nenhuma das três aparece no mapa nem entra na seleção.

CA04 — Segundo polígono soma
Dado 42 OSs selecionadas
Quando desenho um segundo polígono com 10 OSs, sendo 3 já selecionadas
Então o contador mostra 49.

CA05 — Remover uma OS
Dado 42 OSs selecionadas
Quando clico em uma OS selecionada e escolho remover da seleção
Então o contador mostra 41 e o pin volta ao estado normal.

CA06 — Polígono vazio
Dado nenhuma OS apta dentro da área
Quando desenho o polígono
Então a seleção não muda e aparece "Nenhuma OS apta nesta área".

CA07 — Desempenho (RNF-03)
Dado 2.000 OSs aptas no mapa
Quando desenho um polígono que contém 800 delas
Então a seleção e o contador se atualizam em até 1 s, e mover/aproximar o mapa continua fluido.

CA08 — Polo "Todos"
Dado o seletor de polo em "Todos"
Quando abro o Roteirizador
Então a ferramenta de polígono está desabilitada com a orientação "Selecione um polo para montar rotas".

## Fora de escopo
Limpar seleção e contador (HU-031), criar rota (HU-056), atribuir despacho (HU-057), otimização
automática de sequência de visita.

## Dúvidas em aberto
- RNF-03 diz "sem degradação perceptível"; o limite de 1 s do CA07 é proposta (ver lacunas.md).
- A seleção precisa sobreviver a uma troca de tela ou recarga da página?
