---
id: HU-056
titulo: Criar rota a partir das OSs selecionadas
ordem: 45
modulo: Roteirizador
epico: EP-B Planejamento e despacho
tela: "Despacho & Rotas › Roteirizador", modal "Criar Rota"
fase: 2
prioridade: MVP
status: proposta
requisitos: [RF-ROT-03 (proposto)]
regras: [RN-08, RN-09]
nao_funcionais: [RNF-12, RNF-15]
depende_de: [HU-009, HU-012, HU-028]
---

# HU-056 — Criar rota a partir das OSs selecionadas

> **Proposta — validar com o grupo.** Cobre a lacuna entre selecionar OSs (RF-ROT-07) e
> finalizar o planejamento (RF-ROT-16). Baseada no modal "Criar Rota" do protótipo e na
> entidade Rota da ERS §4.

## História
Como **Coordenador de Campo**, quero **criar uma rota com as OSs que selecionei, definindo
equipe, veículo, profissional, ajudante e horários**, para **que cada equipe saia com um roteiro
fechado para o dia**.

## Contexto
As OSs vêm da seleção no mapa (HU-012). Ao salvar, as OSs passam do estado 4 ("Apta a
roteirizar") para o 5 ("Roteirizada"). A rota ainda pode ser alterada até a finalização do
planejamento (HU-013) e a geração do RPA (HU-014, RN-10).

## Regras de negócio
- **RN-08** — só OSs aptas, com coordenada e não desconsideradas.
- **RN-09** — a equipe deve ser do polo das OSs e estar ativa na data da rota.
- **RN-L01** — Campos obrigatórios: nome, data da rota, previsão de início, carregamento e
  equipe/veículo. Opcionais: cor, profissional, ajudante, observação.
- **RN-L02** — Uma OS pertence a no máximo uma rota não finalizada.
- **RN-L03** — A quantidade de OSs da equipe no dia (todas as rotas) não pode exceder a
  capacidade diária da equipe (RF-EQP-01); acima disso, a criação é bloqueada.
- **RN-L04** — Data da rota não pode ser anterior a hoje.

## Critérios de aceite
CA01 — Criar rota (caminho feliz)
Dado 18 OSs aptas selecionadas no Polo 1 e a Equipe A (capacidade 25, ativa, sem rotas no dia)
Quando preencho nome "Bessa manhã", data de amanhã, início 07:30, carregamento 07:00,
Equipe A · QRT-2A18 e salvo
Então a rota é criada com as 18 OSs, que passam a "Roteirizada", a seleção é limpa e aparece o
toast "Rota Bessa manhã criada com 18 OSs".

CA02 — Campo obrigatório
Dado o formulário sem previsão de início
Quando tento salvar
Então o campo é destacado com "Informe a previsão de início" e nada é gravado.

CA03 — Equipe de outro polo (RN-09)
Dado OSs do Polo 1
Quando abro a lista de equipes
Então só aparecem equipes ativas do Polo 1; pela API, uma equipe do Polo 2 retorna `422`.

CA04 — Capacidade excedida (RN-L03)
Dado a Equipe A com capacidade 25 e 10 OSs já em outra rota no mesmo dia
Quando tento criar rota com 18 OSs para ela
Então a criação é bloqueada com "Equipe A: 28 OSs no dia excede a capacidade de 25".

CA05 — OS já em outra rota (RN-L02)
Dado uma das OSs selecionadas já pertence a uma rota não finalizada
Quando tento salvar
Então a criação é bloqueada indicando o número da OS e a rota em que ela está.

CA06 — Data passada
Dado a data da rota de ontem
Quando tento salvar
Então aparece "A data da rota não pode ser anterior a hoje" e nada é gravado.

CA07 — Registro
Dado uma rota criada
Quando consulto a trilha de auditoria
Então aparecem autor, data/hora, a rota e as OSs incluídas (RNF-15).

## Fora de escopo
Atribuição de despacho sem rota (HU-057), sequência ótima de visita, edição e exclusão de rota
(a definir), finalização (HU-013).

## Dúvidas em aberto
- O que significa "carregamento" — horário de retirada do material no almoxarifado?
- Profissional e ajudante são obrigatórios? O protótipo não marca com asterisco.
- Rota pode ser editada ou excluída antes da finalização? Precisa de história própria.
