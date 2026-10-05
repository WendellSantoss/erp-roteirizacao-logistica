---
id: HU-032
titulo: Manter o catálogo de tipos de kit
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: — (sem tela no protótipo; usado no campo "Kit")
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-02]
regras: [RN-11]
nao_funcionais: [RNF-27]
depende_de: [HU-020]
---

# HU-032 — Manter o catálogo de tipos de kit

## História
Como **Administrador**, quero **cadastrar os tipos de kit, os materiais de cada um e quais tipos
de serviço ele atende**, para **que um kit novo entre em uso sem nova versão do sistema (RNF-27)**.

## Regras de negócio
- **RN-L01** — Campos: nome (único), descrição, lista de materiais (texto), tipos de serviço
  atendidos (≥ 1), status.
- **RN-L02** — O vínculo kit ↔ tipo de serviço é o que permite calcular a execução de ontem por
  kit (RN-11).
- **RN-L03** — Tipo de kit com movimentação não é excluído, só inativado.
- **RN-L04** — Carga inicial: Ligação Simples, Hidrômetro, Supressão, Religação.

## Critérios de aceite
CA01 — Cadastrar
Dado o Administrador
Quando cadastra "Kit Corte" vinculado ao tipo de serviço "Corte"
Então o kit aparece no campo "Kit" da saída e no painel de execução de ontem.

CA02 — Nome repetido
Dado "Kit Hidrômetro" cadastrado
Quando cadastro outro com o mesmo nome
Então aparece "Já existe um kit com este nome".

CA03 — Sem tipo de serviço
Dado um kit sem tipo de serviço vinculado
Quando salvo
Então aparece "Vincule ao menos um tipo de serviço" (sem isso a trava não tem como calcular).

CA04 — Inativar
Dado "Kit Supressão" com saídas registradas
Quando inativo
Então ele some do campo "Kit" da saída, mas o histórico continua mostrando o nome.

## Dúvidas em aberto
- Um tipo de serviço pode consumir mais de um kit, ou mais de uma unidade de kit por OS?
