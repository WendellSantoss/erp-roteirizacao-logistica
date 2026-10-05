---
id: HU-004
titulo: Inserir e atualizar OSs sem perder o tratamento feito
modulo: Importação
epico: EP-A Ingestão e preparação de dados
tela: "Importação da OS diária" › resumo "Novas OSs" e "OSs atualizadas (upsert)"
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-IMP-04]
regras: [RN-01, RN-02]
nao_funcionais: [RNF-01, RNF-06, RNF-07]
depende_de: [HU-003, HU-F11]
---

# HU-004 — Inserir e atualizar OSs sem perder o tratamento feito

## História
Como **Analista de Operações**, quero **que a importação diária insira as OSs novas e atualize as
existentes sem apagar a prioridade, a equipe e a desconsideração que já defini**, para **não
refazer todo dia o tratamento do dia anterior ("sem amnésia de registros")**.

## Contexto
A mesma OS aparece em várias planilhas diárias enquanto não é executada. Esta é a regra que
mais pesa na confiabilidade do sistema (RNF-06, RNF-07).

## Regras de negócio
- **RN-01** — Chave: Número da OS + Polo.
- **RN-02** — Prioridade, equipe e desconsideração definidas no GeniOS prevalecem sobre a planilha.
- **RN-L01** — OS nova entra no estado "Pendente" (HU-F11).
- **RN-L02** — OS existente tem os campos vindos do GSAN atualizados (especificação, tipo, prazo,
  setor, quadra etc.); **o estado não retrocede** (uma OS "Roteirizada" continua "Roteirizada").
- **RN-L03** — OS que existia e não veio na planilha do dia **não é apagada nem alterada**.
- **RN-L04** — A importação é tudo ou nada (RNF-07): qualquer erro no upsert desfaz a importação inteira.
- **RN-L05** — Toda OS guarda a importação que a criou e a última que a atualizou.

## Critérios de aceite
CA01 — Novas e atualizadas
Dado 300 OSs já existentes no Polo 1 e uma planilha com essas 300 mais 940 novas
Quando a importação termina
Então há 940 OSs novas em "Pendente", 300 atualizadas, e o resumo mostra "Novas OSs: 940" e
"OSs atualizadas: 300".

CA02 — Tratamento preservado (RN-02)
Dado a OS 4471203 marcada como prioridade e com a Equipe B, e na planilha nova sem prioridade
Quando a importação termina
Então a OS continua prioritária e com a Equipe B, e a especificação foi atualizada com o valor da planilha.

CA03 — Desconsiderada continua desconsiderada
Dado uma OS "Desconsiderada" que volta na planilha
Quando a importação termina
Então ela continua "Desconsiderada" e não aparece em pendências.

CA04 — Estado não retrocede
Dado uma OS "Roteirizada"
Quando volta na planilha com outro prazo
Então o prazo é atualizado e ela continua "Roteirizada".

CA05 — Sem amnésia (RN-L03)
Dado uma OS existente que não está na planilha de hoje
Quando a importação termina
Então a OS continua existindo, sem nenhuma alteração.

CA06 — Tudo ou nada (RNF-07)
Dado uma falha de banco ao gravar a linha 3.000 de 5.000
Quando a importação falha
Então nenhuma OS da planilha foi inserida nem alterada, a importação fica como "falhou" com o
motivo, e o analista pode enviar o arquivo de novo.

CA07 — Mesma OS em outro polo
Dado a OS 4471203 no Polo 1
Quando a planilha do Polo 2 traz a OS 4471203
Então são duas OSs distintas (chave inclui o polo).

CA08 — Desempenho (RNF-01)
Dado a planilha de exemplo com 5.000 linhas e 25 MB
Quando importo
Então validação, filtro e upsert terminam em até 3 min.

CA09 — Reimportar o mesmo arquivo
Dado uma planilha já importada com sucesso
Quando importo o mesmo arquivo de novo
Então 0 OSs novas são criadas e nenhum tratamento é perdido.

## Fora de escopo
Progresso visual (HU-021), captura de coordenadas (HU-005).

## Dúvidas em aberto
- OS que some da planilha do GSAN foi cancelada na concessionária? Se sim, precisaria de um
  estado "Cancelada" que a ERS não prevê.
