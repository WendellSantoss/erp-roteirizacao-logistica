---
id: HU-031
titulo: Ver o contador de OSs selecionadas e limpar a seleção
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › barra "N OSs selecionadas · Limpar"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-ROT-08]
regras: []
nao_funcionais: []
depende_de: [HU-012]
---

# HU-031 — Ver o contador de OSs selecionadas e limpar a seleção

## História
Como **Coordenador de Campo**, quero **ver quantas OSs estão selecionadas e poder limpar tudo de
uma vez**, para **conferir o tamanho da rota antes de criá-la e recomeçar quando errar**.

## Critérios de aceite
CA01 — Contador
Dado 42 OSs selecionadas
Quando olho a barra de seleção
Então vejo "42 OSs selecionadas" e os botões "Limpar", "Atribuir equipe" e "Criar Rota".

CA02 — Limpar
Dado 42 selecionadas
Quando clico em "Limpar"
Então a seleção fica vazia, os pins voltam ao normal e a barra de seleção some.

CA03 — Comparação com capacidade
Dado 42 selecionadas e equipes com capacidade máxima de 25
Quando olho a barra
Então aparece o aviso "Acima da capacidade de qualquer equipe do polo (máx. 25)".

CA04 — Sem seleção
Dado nenhuma OS selecionada
Quando olho a tela
Então "Criar Rota" e "Atribuir equipe" estão desabilitados.
