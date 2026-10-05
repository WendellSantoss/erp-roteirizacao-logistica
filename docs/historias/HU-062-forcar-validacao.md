---
id: HU-062
titulo: Forçar a validação de uma OS reprovada
ordem: 63
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › "Invalidações" › "Forçar validação"
fase: 3
prioridade: MVP
status: proposta
requisitos: [RF-AUD-07 (proposto)]
regras: [RN-14]
nao_funcionais: [RNF-12, RNF-15]
depende_de: [HU-061, HU-020]
---

# HU-062 — Forçar a validação de uma OS reprovada

> **Proposta — validar com o grupo.** Citado em RN-14, RNF-12 e nas atribuições do Gerente de
> Contrato (ERS §2.2), sem requisito próprio.

## História
Como **Gerente de Contrato**, quero **validar uma OS que a fiscalização reprovou, quando a
reprovação foi contestada com sucesso**, para **que ela volte a compor a produção validada e o BM**.

## Regras de negócio
- **RN-14** — OS invalidada só compõe produção validada e BM após validação forçada por perfil autorizado.
- **RN-L01** — Só o Gerente de Contrato.
- **RN-L02** — Justificativa com pelo menos 20 caracteres; fica gravada na Invalidação.
- **RN-L03** — Só com o ciclo aberto.

## Critérios de aceite
CA01 — Forçar
Dado a OS 4471203 "Invalidada" (motivo "Foto ilegível")
Quando o Gerente clica em "Forçar validação" com "Nova foto enviada e aceita pela fiscalização em 12/07"
Então a OS passa a "Validada", entra na produção validada e na prévia do BM, e a trilha registra
autor, data/hora e justificativa.

CA02 — Sem permissão
Dado o Auditor
Quando chama a API de forçar validação
Então recebe `403`; o botão não aparece para ele.

CA03 — Ciclo fechado
Dado o ciclo fechado
Quando o Gerente tenta forçar
Então é recusado com "Ciclo fechado".

CA04 — Justificativa curta
Dado "ok"
Quando o Gerente confirma
Então aparece "Justificativa com pelo menos 20 caracteres".
