---
id: HU-009
titulo: Cadastrar, editar e inativar equipes
modulo: Equipes
epico: EP-B Planejamento e despacho
tela: "Configurações (Equipes)" › cartões de equipe, "Nova equipe", "Editar"
fase: 2
prioridade: MVP
status: rascunho
requisitos: [RF-EQP-01]
regras: []
nao_funcionais: [RNF-15]
depende_de: [HU-028, HU-020, HU-045]
---

# HU-009 — Cadastrar, editar e inativar equipes

## História
Como **Administrador**, quero **manter o cadastro das equipes de campo com veículo, integrantes,
região e capacidade**, para **que o Coordenador monte rotas só com equipes reais e disponíveis**.

## Regras de negócio
- **RN-L01** — Obrigatórios: nome, polo, placa, líder, região de atuação, capacidade diária.
  Opcionais: cor, membros.
- **RN-L02** — Nome único dentro do polo; placa única no sistema; placa no padrão antigo
  (`ABC-1234`) ou Mercosul (`ABC1D23`).
- **RN-L03** — Capacidade diária: inteiro de 1 a 99 OSs.
- **RN-L04** — O líder e os membros vêm do cadastro de profissionais e ajudantes do mesmo polo (HU-028).
- **RN-L05** — Equipe não é excluída, só inativada; inativa não aparece para novas rotas.
- **RN-L06** — Toda alteração vai para a trilha (RNF-15), que é o "histórico da equipe".

## Critérios de aceite
CA01 — Cadastrar
Dado um Administrador no Polo 1
Quando cadastra "Equipe F", cor azul, placa QRT2A19, líder J. Andrade, membros M. Souza e D. Lima,
região "Bessa / Manaíra", capacidade 25
Então a equipe aparece como cartão ativo do Polo 1 com esses dados.

CA02 — Duplicidade
Dado a "Equipe A" no Polo 1 e a placa QRT-2A18 em uso
Quando cadastro outra "Equipe A" no Polo 1, ou outra equipe com a placa QRT-2A18
Então o cadastro é recusado com "Já existe equipe com este nome neste polo" ou "Placa já cadastrada".

CA03 — Validações
Dado capacidade 0 ou placa "12345"
Quando salvo
Então os campos são destacados com o motivo e nada é gravado.

CA04 — Editar
Dado a Equipe A com capacidade 20
Quando altero para 25
Então a alteração vale para rotas criadas a partir de agora, e a trilha guarda 20 → 25.

CA05 — Inativar
Dado a Equipe C ativa sem rotas em aberto
Quando inativo
Então ela fica com status "Inativa" e não aparece na lista de equipes ao criar rota.

CA06 — Permissão
Dado um Coordenador de Campo
Quando tenta cadastrar ou editar equipe
Então não vê os botões e a API responde `403`.

## Fora de escopo
Bloqueio de inativação com rota aberta (HU-029), vínculo com polo (HU-010).
