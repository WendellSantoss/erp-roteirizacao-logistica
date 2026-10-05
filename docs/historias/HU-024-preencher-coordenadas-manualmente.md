---
id: HU-024
titulo: Informar a coordenada de uma unidade manualmente
ordem: 32
modulo: Webscraper
epico: EP-A Ingestão e preparação de dados
tela: — (sem tela no protótipo)
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-WEB-04]
regras: [RN-04]
nao_funcionais: [RNF-15]
depende_de: [HU-023]
---

# HU-024 — Informar a coordenada de uma unidade manualmente

## História
Como **Analista de Operações**, quero **digitar ou marcar no mapa a coordenada de uma unidade que
a captura não resolveu**, para **liberar as OSs dessa unidade para roteirização**.

## Regras de negócio
- **RN-L01** — Mesma validação de área da HU-005 (RN-L02).
- **RN-L02** — Coordenada informada manualmente **não é sobrescrita** por capturas automáticas
  posteriores; só por outra edição manual.
- **RN-L03** — A edição fica na trilha com valor anterior, novo, autor e data/hora (RNF-15).

## Critérios de aceite
CA01 — Digitar coordenada
Dado a unidade "Bessa" sem coordenada
Quando informo latitude −7,0832 e longitude −34,8336 e salvo
Então a unidade fica com essa coordenada marcada como "manual", sai da lista de falhas e as OSs
dela passam a aparecer no mapa.

CA02 — Marcar no mapa
Dado a mesma unidade
Quando clico no mapa no ponto desejado
Então latitude e longitude são preenchidas com o ponto clicado, para eu confirmar.

CA03 — Fora da área
Dado latitude −23,5
Quando tento salvar
Então aparece "Coordenada fora da área de operação (Paraíba)" e nada é gravado.

CA04 — Formato brasileiro
Dado que digito "-7,0832" (vírgula) ou "-7.0832" (ponto)
Quando salvo
Então os dois formatos são aceitos.

CA05 — Manual prevalece
Dado uma unidade com coordenada manual
Quando a captura automática roda de novo
Então a coordenada manual não é alterada.
