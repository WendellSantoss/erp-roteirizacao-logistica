---
id: HU-002
titulo: Validar o layout da planilha antes de importar
ordem: 16
modulo: Importação
epico: EP-A Ingestão e preparação de dados
tela: "Importação da OS diária" › Log de alertas
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-IMP-02]
regras: []
nao_funcionais: [RNF-07, RNF-19]
depende_de: [HU-001]
---

# HU-002 — Validar o layout da planilha antes de importar

## História
Como **Analista de Operações**, quero **que o sistema confira se a planilha segue o layout do
GSAN antes de processar qualquer OS**, para **saber exatamente o que corrigir em vez de descobrir
depois que a carteira foi importada pela metade ou com colunas trocadas**.

## Contexto
Roda logo após o recebimento do arquivo (HU-001) e antes do filtro de escopo (HU-003). O layout
do GSAN é premissa estável (PR-01); mudança de layout exige manutenção no parser.

## Regras de negócio
- **RN-L01** — Colunas obrigatórias (nomes do cabeçalho do GSAN): Ordem de Serviço,
  Especificação, Tipo, Nº do Imóvel, Data de Geração, Unidade Atual, Cidade, Setor, Quadra,
  Prazo (h), Abertura. *(lista a confirmar com uma planilha real — ver dúvidas)*
- **RN-L02** — **Coluna obrigatória ausente → o arquivo inteiro é recusado.** Nada é gravado.
- **RN-L03** — **Linha inválida → só a linha é ignorada** e vira alerta no log da importação.
  Linha inválida: Ordem de Serviço vazia, data de geração/abertura que não é data, prazo que não
  é número positivo, ou OS repetida dentro do mesmo arquivo (a segunda ocorrência é ignorada).
- **RN-L04** — Colunas extras são ignoradas sem erro; a ordem das colunas não importa.

## Critérios de aceite
CA01 — Planilha válida
Dado uma planilha com todas as colunas obrigatórias e 1.324 linhas válidas
Quando a validação roda
Então a importação segue para o filtro de escopo sem alertas.

CA02 — Coluna ausente
Dado uma planilha sem as colunas "Setor" e "Quadra"
Quando a validação roda
Então a importação é recusada com "Colunas obrigatórias ausentes: Setor, Quadra", nenhuma OS é
gravada e a importação fica registrada como "recusada" com o motivo.

CA03 — Linhas inválidas
Dado uma planilha válida com 3 linhas inválidas (linha 15 sem número de OS, linha 230 com
abertura "31/02/2026", linha 900 com prazo "-4")
Quando a importação termina
Então as demais linhas são importadas e o log mostra 3 alertas, cada um com o número da linha,
o campo e o motivo.

CA04 — OS repetida no arquivo
Dado a OS 4471203 em duas linhas do mesmo arquivo
Quando a importação termina
Então apenas a primeira é considerada e há um alerta "OS 4471203 repetida na linha N".

CA05 — Ordem e colunas extras
Dado uma planilha com as colunas em outra ordem e uma coluna extra "Observação GSAN"
Quando a validação roda
Então a importação segue normalmente.

CA06 — Arquivo corrompido
Dado um `.xlsx` que não abre (arquivo truncado)
Quando a validação roda
Então a importação é recusada com "Não foi possível ler a planilha. Gere o arquivo novamente no GSAN".

## Fora de escopo
Filtro de escopo (HU-003), upsert (HU-004).

## Dúvidas em aberto
- Precisamos de uma planilha GSAN real anonimizada para fechar a lista de colunas e os formatos de data.
- Em qual aba da planilha estão os dados? (assumido: a primeira)
