---
id: HU-060
titulo: Liberar OSs tratadas para roteirização
modulo: Pendências
epico: EP-A Ingestão e preparação de dados
tela: "Gerenciar Pendências" (ação ainda não desenhada no protótipo)
fase: 1
prioridade: MVP
status: proposta
requisitos: [RF-PEN-06 (proposto)]
regras: [RN-04, RN-08]
nao_funcionais: [RNF-15]
depende_de: [HU-006, HU-F11]
---

# HU-060 — Liberar OSs tratadas para roteirização

> **Proposta — validar com o grupo.** A ERS define o estado "Apta a roteirizar" como "tratamento
> concluído e coordenadas presentes", mas nenhum requisito diz quem conclui o tratamento nem como.

## História
Como **Analista de Operações**, quero **marcar como prontas as OSs que já tratei**, para **que
elas apareçam no mapa do Coordenador de Campo**.

## Regras de negócio
- **RN-04** — OS sem coordenada válida não pode ser liberada.
- **RN-L01** — Liberação individual ou em lote (OSs marcadas na lista).
- **RN-L02** — Em lote, as OSs sem coordenada são puladas e informadas; as demais são liberadas.

## Critérios de aceite
CA01 — Liberar em lote
Dado 30 OSs pendentes marcadas, todas com coordenada
Quando clico em "Liberar para roteirização"
Então as 30 passam a "Apta a roteirizar", saem da lista e aparecem no mapa do Roteirizador.

CA02 — Lote com OS sem coordenada
Dado 30 marcadas, 4 delas sem coordenada
Quando libero
Então 26 são liberadas e aparece "4 OSs não liberadas: sem coordenada" com os números.

CA03 — Registro
Dado OSs liberadas
Quando consulto a trilha
Então cada OS tem a transição com autor e data/hora.

## Dúvidas em aberto
- O tratamento exige mais alguma coisa além de coordenada (ex.: prioridade definida, tipo de
  equipe definido)? Se não exigir, a liberação pode ser **automática** quando a OS tem
  coordenada — e esta história vira só a regra.
