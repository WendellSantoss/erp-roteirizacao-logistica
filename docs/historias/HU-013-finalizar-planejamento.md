---
id: HU-013
titulo: Finalizar o planejamento do dia
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador" › botão "Finalizar"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-ROT-16]
regras: [RN-08, RN-09]
nao_funcionais: [RNF-15, RNF-17]
depende_de: [HU-056, HU-057]
---

# HU-013 — Finalizar o planejamento do dia

## História
Como **Coordenador de Campo**, quero **fechar o planejamento de uma operação e data depois de
conferir que todas as rotas estão consistentes**, para **liberar a geração do despacho (RPA)**.

## Regras de negócio
- **RN-L01** — O planejamento é identificado por polo + operação + data.
- **RN-L02** — Só finaliza se **todas** as rotas tiverem: equipe ativa do polo (RN-09), ao menos
  1 OS, campos obrigatórios preenchidos, total do dia por equipe dentro da capacidade, e todas as
  OSs ainda em "Roteirizada" (nenhuma desconsiderada no meio do caminho).
- **RN-L03** — Planejamento finalizado não aceita novas rotas nem alterações de rota.
- **RN-L04** — Registra data/hora e autor da finalização.

## Critérios de aceite
CA01 — Finalizar
Dado o planejamento Polo 1 · PSS · 12/07 com 4 rotas válidas e 92 OSs
Quando clico em "Finalizar" e confirmo o resumo (4 rotas, 92 OSs, equipes)
Então o planejamento fica "Finalizado", com data/hora e autor, e "Gerar arquivo RPA" fica habilitado.

CA02 — Inconsistência bloqueia
Dado uma rota sem OS e outra cuja equipe foi inativada
Quando clico em "Finalizar"
Então a finalização é recusada e aparece a lista das inconsistências, cada uma com a rota e o
motivo; nada muda.

CA03 — Bloqueado após finalizar
Dado o planejamento finalizado
Quando tento criar rota ou mover OS entre rotas
Então a ação é recusada com "Planejamento finalizado".

CA04 — Sem rotas
Dado um planejamento sem nenhuma rota
Quando clico em "Finalizar"
Então aparece "Não há rotas para finalizar".

## Dúvidas em aberto
- É possível reabrir um planejamento finalizado antes de gerar o RPA? Proposta: sim, pelo
  Coordenador, com registro na trilha.
