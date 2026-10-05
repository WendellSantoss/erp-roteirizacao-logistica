---
id: HU-005
titulo: Capturar as coordenadas das unidades no portal GSAN
modulo: Webscraper
epico: EP-A Ingestão e preparação de dados
tela: Cabeçalho › "Webscraper — Capturando coords."
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-WEB-01]
regras: [RN-04, RN-05]
nao_funcionais: [RNF-05, RNF-13, RNF-28]
depende_de: [HU-004, HU-F08]
---

# HU-005 — Capturar as coordenadas das unidades no portal GSAN

## História
Como **Analista de Operações**, quero **que o sistema busque sozinho a latitude e a longitude
das unidades no portal do GSAN**, para **que as OSs apareçam no mapa sem eu digitar coordenadas**.

## Contexto
Sem coordenada válida a OS não vai para o mapa (RN-04). O acesso ao portal depende de
credenciais válidas e da estabilidade do portal (PR-03).

## Regras de negócio
- **RN-05** — Respeitar o limite de requisições do portal e a LGPD.
- **RN-L01** — No máximo 1 requisição por segundo ao portal (proposta até sabermos o limite real).
- **RN-L02** — Coordenada válida: latitude entre −8,5 e −6,0 e longitude entre −38,8 e −34,7
  (área da Paraíba). Fora disso é rejeitada como inválida.
- **RN-L03** — A captura roda automaticamente ao final de cada importação, só para unidades sem
  coordenada válida (ver cache, HU-046), e também pode ser disparada manualmente.
- **RN-L04** — Credenciais do portal ficam em segredo do servidor, nunca no código nem no frontend.
- **RN-L05** — Do portal só se grava a coordenada da unidade; nenhum dado de titular é armazenado.

## Critérios de aceite
CA01 — Captura após importação
Dado uma importação concluída com 120 unidades sem coordenada
Quando a captura termina
Então as unidades capturadas têm latitude e longitude gravadas, e as OSs delas passam a ter
coordenada.

CA02 — Coordenada fora da área
Dado o portal retornando latitude −23,5 para uma unidade
Quando a captura processa a unidade
Então a coordenada não é gravada e a unidade entra na lista de falhas com motivo "Coordenada fora da área de operação".

CA03 — Limite de requisições
Dado 120 unidades a capturar
Quando a captura roda
Então nunca há mais de 1 requisição por segundo ao portal (verificado no log técnico).

CA04 — Portal fora do ar
Dado o portal inacessível
Quando a captura tenta a primeira unidade
Então tenta 3 vezes com espera crescente, depois encerra com "Portal GSAN indisponível", e as
unidades ficam como pendentes de captura (não como falha definitiva).

CA05 — Não bloqueia (RNF-05)
Dado uma captura em andamento
Quando uso qualquer outra tela
Então o sistema responde normalmente.

CA06 — Credencial inválida
Dado credenciais do portal expiradas
Quando a captura inicia
Então encerra com "Credenciais do portal GSAN inválidas — avise o Administrador" e nada é gravado.

## Fora de escopo
Indicador no cabeçalho (HU-022), reprocessamento de falhas (HU-023), coordenada manual (HU-024), cache (HU-046).

## Dúvidas em aberto
- Qual é a URL e o fluxo de navegação do portal? Precisamos de acesso de teste.
- O portal tem limite de requisições documentado ou termos de uso que proíbam automação?
