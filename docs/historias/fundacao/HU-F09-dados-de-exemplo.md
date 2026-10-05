---
id: HU-F09
titulo: Gerar dados de exemplo anonimizados
ordem: 9
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-14]
depende_de: [HU-F03]
---

# HU-F09 — Gerar dados de exemplo anonimizados

## História
Como **desenvolvedor do GeniOS**, quero **planilhas GSAN fictícias e uma carga inicial do banco
com polos, unidades, equipes e kits**, para **testar e demonstrar o sistema sem usar dados
reais de imóveis e titulares (RNF-14)**.

## Critérios de aceite
CA01 — Planilha GSAN fictícia
Dado `backend/fixtures/gsan/`
Quando listo
Então existem: uma planilha válida com 5.000 linhas (cenário do RNF-01), uma com coluna
obrigatória ausente, uma com OSs fora de escopo e uma de execução/fechamento — todas com o
layout do GSAN e nenhum dado real.

CA02 — Carga inicial
Dado o banco vazio
Quando executo o comando de carga
Então existem os 3 polos (Central, Norte, Sul), unidades com coordenadas em João Pessoa e
região, ao menos 5 equipes por polo, os 4 tipos de kit, operações PSS / XPT Express / Litoral e
um usuário por perfil da ERS.

CA03 — Nada real
Dado as fixtures
Quando procuro CPF, nome de titular ou endereço real
Então não encontro; nomes e endereços são gerados.

## Dúvidas em aberto
- Precisamos de uma planilha GSAN real **anonimizada** para copiar o layout exato das colunas.
