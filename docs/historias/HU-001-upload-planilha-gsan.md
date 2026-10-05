---
id: HU-001
titulo: Enviar a planilha diária do GSAN
modulo: Importação
epico: EP-A Ingestão e preparação de dados
tela: "Importação da OS diária" (docs/design/prototipo/GeniOS ERP.html)
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-IMP-01]
regras: []
nao_funcionais: [RNF-05, RNF-19, RNF-25]
depende_de: [HU-F04, HU-F08, HU-019]
---

# HU-001 — Enviar a planilha diária do GSAN

## História
Como **Analista de Operações**, quero **enviar a planilha bruta do GSAN arrastando o arquivo
ou selecionando-o**, para **iniciar a importação diária das OSs sem depender de outra pessoa**.

## Contexto
É a porta de entrada do ciclo de vida da OS (estado 1, "Importada"). Esta história cobre só o
**recebimento** do arquivo; validar o layout (HU-002), filtrar escopo (HU-003), fazer o upsert
(HU-004) e mostrar o progresso (HU-021) são histórias seguintes. No protótipo, é a tela
"Importação da OS diária".

## Regras de negócio
- **RN-L01** — Aceita apenas um arquivo por envio, com extensão `.xlsx`.
- **RN-L02** — Tamanho máximo de 25 MB (ver dúvida sobre a unidade).
- **RN-L03** — Só os perfis Analista de Operações e Administrador podem enviar (RF-TRV-02).
- **RN-L04** — O envio exige um polo selecionado; com "Todos" a área de envio fica desabilitada
  (ERS §2.3).

## Critérios de aceite
CA01 — Envio por seleção (caminho feliz)
Dado um Analista de Operações com o Polo 1 – Central selecionado
Quando seleciona `gsan_os_2026-07-11.xlsx` de 4 MB e confirma
Então o arquivo é recebido, a importação é registrada com nome do arquivo, usuário, polo e
data/hora, e a tela passa para o acompanhamento da importação.

CA02 — Envio por arrastar e soltar
Dado a mesma situação do CA01
Quando arrasta o arquivo para a área de envio
Então o comportamento é idêntico ao CA01, e a área destaca visualmente que o arquivo pode ser solto.

CA03 — Extensão inválida
Dado um arquivo `gsan.csv` ou `gsan.xls`
Quando tento enviar
Então o envio é recusado antes do upload com a mensagem "Formato não aceito: envie a planilha
do GSAN em .xlsx" e nenhuma importação é registrada.

CA04 — Arquivo acima do limite
Dado um `.xlsx` de 26 MB
Quando tento enviar
Então o envio é recusado com a mensagem "Arquivo com 26 MB excede o limite de 25 MB" e nenhuma
importação é registrada.

CA05 — Limite também no servidor
Dado uma chamada direta à API com arquivo de 26 MB ou extensão diferente de `.xlsx`
Quando o servidor recebe
Então responde `400` com o mesmo motivo do CA03/CA04; a validação não depende só da tela.

CA06 — Polo "Todos"
Dado o seletor de polo em "Todos"
Quando abro a tela de importação
Então a área de envio está desabilitada com a orientação "Selecione um polo para importar".

CA07 — Perfil sem permissão
Dado um usuário Almoxarife
Quando tenta acessar a tela ou chamar a API de importação
Então não vê o item de menu e a API responde `403`.

CA08 — Mais de um arquivo
Dado dois arquivos arrastados juntos
Quando solto na área de envio
Então nada é enviado e aparece "Envie um arquivo por vez".

## Fora de escopo
Validação de colunas (HU-002), filtro de escopo (HU-003), upsert (HU-004), progresso (HU-021),
envio automatizado sem usuário (ERS §5 cita "upload manual ou automatizado" — fora do MVP).

## Dúvidas em aberto
- 25 MB = 25.000.000 ou 26.214.400 bytes? Proposta: 26.214.400 (25 MiB).
- Pode haver mais de uma importação do mesmo polo no mesmo dia? (afeta HU-004)
