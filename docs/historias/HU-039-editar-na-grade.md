---
id: HU-039
titulo: Corrigir dados da execução direto na grade
ordem: 56
modulo: Auditoria
epico: EP-D Fechamento, auditoria e faturamento
tela: "Auditoria & Fechamento" › "Grade de auditoria" (edição inline)
fase: 3
prioridade: MVP
status: rascunho
requisitos: [RF-AUD-04]
regras: [RN-14, RN-15, RN-16]
nao_funcionais: [RNF-04, RNF-18]
depende_de: [HU-038, HU-040]
---

# HU-039 — Corrigir dados da execução direto na grade

## História
Como **Auditor / Faturista**, quero **clicar numa célula e corrigir serviço, equipe, foto, status
ou valor sem abrir outra tela**, para **revisar centenas de OSs por dia em pouco tempo (RNF-18)**.

## Regras de negócio
- **RN-L01** — Status editável: Executada → Validada (aprovação na auditoria). Invalidada →
  Validada **não** é feito aqui (é a HU-062, forçar validação).
- **RN-L02** — Alterar o Serviço recalcula o Valor pela tabela de preços (RN-16).
- **RN-L03** — Editar o Valor manualmente exige justificativa (o valor deixa de seguir a tabela).
- **RN-L04** — Ciclo fechado → nada é editável (RN-15).
- **RN-L05** — Esc cancela a edição; Enter ou sair da célula salva.

## Critérios de aceite
CA01 — Validar OS
Dado a OS 4471203 "Executada"
Quando mudo o status para "Validada" na célula
Então a alteração é salva e confirmada em até 1 s (RNF-04) e a OS passa a contar na produção validada.

CA02 — Trocar serviço
Dado a OS com serviço "Religação" (R$ 80,00)
Quando troco para "Ligação Simples" (R$ 250,00 na tabela vigente)
Então o Valor passa a R$ 250,00 automaticamente.

CA03 — Valor manual
Dado a OS com R$ 250,00
Quando digito R$ 200,00
Então é pedida uma justificativa; sem ela, a edição é cancelada.

CA04 — Invalidada
Dado uma OS "Invalidada"
Quando tento mudar o status na célula
Então a opção "Validada" não está disponível e aparece a dica "Use Forçar validação".

CA05 — Erro ao salvar
Dado uma falha de rede ao salvar
Quando a edição falha
Então a célula volta ao valor anterior e mostra "Não foi possível salvar — tente novamente".

CA06 — Ciclo fechado
Dado o ciclo fechado
Quando clico numa célula
Então ela não entra em edição.
