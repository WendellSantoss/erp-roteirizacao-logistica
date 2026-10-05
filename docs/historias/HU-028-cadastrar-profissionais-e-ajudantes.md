---
id: HU-028
titulo: Cadastrar profissionais e ajudantes
ordem: 39
modulo: Equipes
epico: EP-B Planejamento e despacho
tela: — (sem tela no protótipo; usada nos campos Líder, Membros, Profissional e Ajudante)
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-EQP-04]
regras: []
nao_funcionais: [RNF-14]
depende_de: [HU-020]
---

# HU-028 — Cadastrar profissionais e ajudantes

## História
Como **Administrador**, quero **cadastrar as pessoas que podem compor as equipes, dizendo se são
profissionais ou ajudantes**, para **que equipes e rotas só usem pessoas habilitadas**.

## Regras de negócio
- **RN-L01** — Campos: nome, matrícula (única), função (Profissional ou Ajudante), polo, status.
- **RN-L02** — Uma pessoa está em no máximo uma equipe ativa por vez.
- **RN-L03** — Pessoa inativa não aparece para seleção; não é excluída.
- **RN-L04** — Só o necessário (RNF-14): não cadastrar CPF, telefone ou endereço.

## Critérios de aceite
CA01 — Cadastrar
Dado o Administrador no Polo 1
Quando cadastra "J. Andrade", matrícula 1023, Profissional
Então ele aparece como opção de líder/profissional nas equipes e rotas do Polo 1.

CA02 — Matrícula repetida
Dado a matrícula 1023 em uso
Quando cadastro outra pessoa com 1023
Então aparece "Matrícula já cadastrada".

CA03 — Uma equipe por vez
Dado M. Souza na Equipe A ativa
Quando tento colocá-la na Equipe B
Então aparece "M. Souza já está na Equipe A".

CA04 — Função respeitada
Dado o campo "Ajudante" na criação de rota
Quando abro a lista
Então só aparecem pessoas com função Ajudante, ativas, do polo.
