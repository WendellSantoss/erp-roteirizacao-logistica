---
id: HU-052
titulo: Executar operações a partir de sugestões do assistente
modulo: Assistente
epico: EP-E Inteligência e suporte à decisão
tela: "Assistente GeniOS" › sugestão "Atribuir despacho"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ASS-04]
regras: [RN-21]
nao_funcionais: [RNF-12]
depende_de: [HU-050, HU-053, HU-057]
---

# HU-052 — Executar operações a partir de sugestões do assistente

## História
Como **Coordenador de Campo**, quero **que o assistente sugira ações e as execute para mim**,
para **resolver tarefas como "atribuir estas OSs à Equipe B" com uma frase**.

## Regras de negócio
- **RN-21** — A ação passa pelas mesmas validações e travas do módulo (mesmo serviço do backend).
- **RN-L01** — Ações disponíveis no MVP: atribuir despacho (HU-057), marcar prioridade (HU-058).
  Ações críticas (RNF-12: forçar validação, desconsiderar, liberar trava, reabrir ciclo) **não**
  podem ser executadas pelo assistente.
- **RN-L02** — Toda ação vai para a confirmação (HU-053) antes de executar.
- **RN-L03** — A trilha registra a ação como "via assistente".

## Critérios de aceite
CA01 — Sugestão
Dado 12 OSs selecionadas no polígono
Quando pergunto "pra quem eu mando essas OSs?"
Então o assistente sugere equipes com capacidade livre e oferece o botão "Atribuir despacho".

CA02 — Mesmas regras
Dado a Equipe A sem capacidade
Quando peço "atribui essas 12 para a Equipe A"
Então o assistente informa a mesma recusa da tela ("excede a capacidade de 25").

CA03 — Ação crítica
Dado o Gerente
Quando pede "força a validação da OS 4471203"
Então o assistente explica que a ação deve ser feita na tela de Invalidações e oferece o link.

CA04 — Permissão
Dado o Almoxarife
Quando pede "atribui as OSs à Equipe B"
Então o assistente informa que o perfil dele não permite essa ação.
