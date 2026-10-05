---
id: HU-016
titulo: Bloquear saída de kit acima da execução anterior
ordem: 68
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › Saída de kit e diálogo "Saída bloqueada"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-03, RF-ALM-04]
regras: [RN-11, RN-13]
nao_funcionais: [RNF-08, RNF-12, RNF-19]
depende_de: [HU-015, HU-018, HU-066]
---

# HU-016 — Bloquear saída de kit acima da execução anterior

## História
Como **Almoxarife**, quero **que o sistema impeça a saída de kits acima do que foi executado no
dia anterior**, para **que o material entregue às equipes acompanhe a produção real e não vire
estoque perdido em campo**.

## Contexto
É a "trava de histórico". A execução do dia anterior vem da planilha de execução conciliada
(HU-018), que traz OSs por **tipo de serviço**; o vínculo tipo de serviço → kit vem da
parametrização (HU-066). O registro da saída em si é a HU-015; esta história é o bloqueio.
A liberação excepcional é a HU-063.

## Regras de negócio
- **RN-11** — `quantidade_saída(kit, D) ≤ quantidade_executada(kit, D−1)` no mesmo polo.
- **RNF-08** — A trava é aplicada no servidor; nenhuma chamada à API a contorna.
- **RN-L01** — `quantidade_saída(kit, D)` é a **soma** de todas as saídas daquele kit no polo no
  dia D, incluindo a que está sendo registrada (proposta — ver dúvidas).
- **RN-L02** — Sem execução registrada em D−1 para o kit, o limite é 0 e a saída é bloqueada
  (liberável pela HU-063).
- **RN-L03** — Duas saídas simultâneas não podem, juntas, ultrapassar o limite.

## Critérios de aceite
CA01 — Dentro do limite (caminho feliz)
Dado o Polo 1 com 10 "Kit Hidrômetro" executados ontem e nenhuma saída hoje
Quando registro saída de 10 para a Equipe A
Então a saída é registrada e o painel mostra 0 restante para hoje.

CA02 — Acima do limite
Dado o CA01 concluído
Quando registro mais 1 "Kit Hidrômetro" para a Equipe B
Então a saída **não** é registrada, o saldo não muda e aparece a mensagem de bloqueio com
"Kit Hidrômetro · Solicitado hoje: 11 un. · Executado ontem: 10 un." (RF-ALM-04).

CA03 — Soma do dia
Dado 10 executados ontem
Quando registro 6 para a Equipe A e depois 5 para a Equipe B
Então a primeira é aceita e a segunda bloqueada, informando "Solicitado hoje: 11 un.".

CA04 — Sem histórico
Dado nenhum "Kit Supressão" executado ontem no polo
Quando registro saída de 1
Então a saída é bloqueada informando "Executado ontem: 0 un.".

CA05 — Limite é por polo
Dado 10 executados ontem no Polo 1 e 0 no Polo 2
Quando registro 5 no Polo 2
Então é bloqueada; a execução do Polo 1 não conta para o Polo 2.

CA06 — Contorno pela API (RNF-08)
Dado o CA01 concluído
Quando envio direto à API uma saída de 1 "Kit Hidrômetro" no Polo 1
Então a API responde `422` com o mesmo motivo e nada é gravado.

CA07 — Concorrência (RN-L03)
Dado 10 executados ontem e nenhuma saída hoje
Quando duas saídas de 6 chegam ao mesmo tempo
Então exatamente uma é aceita e a outra bloqueada.

CA08 — Tentativa registrada
Dado qualquer bloqueio
Quando consulto a trilha de auditoria (HU-045)
Então a tentativa aparece com usuário, data/hora, kit, quantidade solicitada e limite.

## Fora de escopo
Registro da saída (HU-015), mensagem/diálogo de bloqueio no visual do protótipo (HU-033),
liberação excepcional (HU-063), painel de execução de ontem (HU-034).

## Dúvidas em aberto
- **D−1 é o dia anterior corrido ou o último dia com execução?** Na segunda-feira, "ontem" é
  domingo. Proposta: último dia útil.
- A trava compara a soma do dia (RN-L01) ou cada saída isolada? A fórmula da ERS sugere a soma.
- O cancelamento de uma saída devolve a quantidade ao limite do dia?
