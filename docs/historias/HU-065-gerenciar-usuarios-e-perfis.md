---
id: HU-065
titulo: Gerenciar usuários, perfis e polos de acesso
ordem: 22
modulo: Transversal
epico: EP-F Requisitos transversais
tela: — (a desenhar)
fase: 1
prioridade: MVP
status: proposta
requisitos: [RF-TRV-06 (proposto)]
regras: []
nao_funcionais: [RNF-11, RNF-15]
depende_de: [HU-019, HU-020]
---

# HU-065 — Gerenciar usuários, perfis e polos de acesso

> **Proposta — validar com o grupo.** A ERS §2.2 diz que o Administrador "cadastra usuários e
> perfis", mas não há requisito.

## História
Como **Administrador**, quero **criar usuários, definir o perfil e os polos de cada um, e
desativá-los**, para **dar e tirar acesso sem mexer no banco de dados**.

## Regras de negócio
- **RN-L01** — Campos: nome, e-mail (único), perfil (um dos 6 da ERS), polos permitidos (≥ 1; Gerente = todos), status.
- **RN-L02** — Usuário não é excluído, só desativado (a trilha precisa do autor).
- **RN-L03** — Senha inicial temporária, troca obrigatória no primeiro acesso.
- **RN-L04** — O Administrador não pode desativar a si mesmo nem remover o último Administrador.

## Critérios de aceite
CA01 — Criar
Dado o Administrador
Quando cria "Carla Lima", carla@genios.local, Auditor, Polo 1
Então ela consegue entrar com a senha temporária, é obrigada a trocá-la, e vê só o que o Auditor do Polo 1 vê.

CA02 — E-mail repetido
Dado o e-mail em uso
Quando crio outro usuário com ele
Então aparece "E-mail já cadastrado".

CA03 — Desativar
Dado a Carla logada
Quando o Administrador a desativa
Então a próxima requisição dela recebe `401` e ela não consegue entrar de novo.

CA04 — Último Administrador
Dado um único Administrador ativo
Quando tenta mudar o próprio perfil ou se desativar
Então é recusado com "Deve existir ao menos um Administrador ativo".
