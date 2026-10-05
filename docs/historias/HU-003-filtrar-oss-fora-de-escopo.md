---
id: HU-003
titulo: Descartar OSs fora do escopo contratual
ordem: 24
modulo: Importação
epico: EP-A Ingestão e preparação de dados
tela: "Importação da OS diária" › resumo "Ignorados (fora de escopo)"
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-IMP-03]
regras: [RN-03]
nao_funcionais: []
depende_de: [HU-002, HU-066]
---

# HU-003 — Descartar OSs fora do escopo contratual

## História
Como **Analista de Operações**, quero **que as OSs de unidades fora do contrato sejam descartadas
automaticamente na importação**, para **trabalhar só com a carteira que a empresa é paga para
executar, sem limpar a planilha à mão**.

## Contexto
A planilha bruta do GSAN traz OSs de todas as unidades. A lista de unidades do escopo é um
parâmetro do sistema (HU-066). O polo da OS vem do cadastro da unidade.

## Regras de negócio
- **RN-03** — OS fora de escopo não é persistida na carteira, mas entra no resumo e no log.
- **RN-L01** — Uma OS está no escopo se a sua "Unidade Atual" está cadastrada como unidade do
  escopo **do polo selecionado** na importação.
- **RN-L02** — Unidade que não existe no cadastro conta como fora de escopo e gera alerta
  "Unidade X não cadastrada" (pode ser unidade nova do contrato).

## Critérios de aceite
CA01 — Descarte com resumo
Dado uma planilha de 1.326 linhas válidas, 86 delas de unidades fora do escopo do Polo 1
Quando a importação termina
Então 1.240 OSs seguem para o upsert, 86 não são gravadas e o resumo mostra "Ignorados (fora de
escopo): 86".

CA02 — Detalhe no log
Dado o CA01
Quando abro o log da importação
Então vejo as 86 OSs descartadas agrupadas por unidade, com a quantidade de cada uma.

CA03 — Unidade desconhecida
Dado uma linha com a unidade "Jardim Novo", que não está cadastrada
Quando a importação termina
Então a OS é descartada e há o alerta "Unidade Jardim Novo não cadastrada — 12 OSs ignoradas".

CA04 — Escopo de outro polo
Dado a importação feita no Polo 1 e uma OS de unidade do escopo do Polo 2
Quando a importação termina
Então a OS é descartada como fora de escopo do Polo 1.

CA05 — Nada a importar
Dado uma planilha em que todas as OSs estão fora do escopo
Quando a importação termina
Então nenhuma OS é gravada e o resumo diz "Nenhuma OS do escopo do Polo 1 nesta planilha".

## Fora de escopo
Cadastro das unidades do escopo (HU-066).

## Dúvidas em aberto
- A planilha do GSAN é separada por polo, ou uma planilha traz os três polos? Se traz os três,
  a importação deveria distribuir as OSs por polo em vez de exigir polo selecionado.
