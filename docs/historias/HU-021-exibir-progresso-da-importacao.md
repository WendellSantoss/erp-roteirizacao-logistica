---
id: HU-021
titulo: Acompanhar o progresso da importação
modulo: Importação
epico: EP-A Ingestão e preparação de dados
tela: "Importação da OS diária" › "Processando planilha GSAN…" e "Importação concluída"
fase: 1
prioridade: MVP
status: rascunho
requisitos: [RF-IMP-05]
regras: []
nao_funcionais: [RNF-01, RNF-05]
depende_de: [HU-001, HU-F08]
---

# HU-021 — Acompanhar o progresso da importação

## História
Como **Analista de Operações**, quero **ver em tempo real em que etapa e em que percentual está
a importação**, para **saber se ela está andando e quando posso começar o tratamento, sem ficar
preso na tela**.

## Regras de negócio
- **RN-L01** — Etapas, nesta ordem: Validando layout → Filtrando escopo → Gravando OSs → Concluída.
- **RN-L02** — O percentual é atualizado a cada 5% de avanço, no mínimo (RNF-01).

## Critérios de aceite
CA01 — Progresso
Dado uma importação de `gsan_os_2026-07-11.xlsx` com 1.324 linhas em andamento
Quando olho a tela
Então vejo nome do arquivo, total de linhas, percentual e etapa atual, atualizados ao menos a
cada 5% de avanço.

CA02 — Navegação livre (RNF-05)
Dado uma importação em andamento
Quando navego para Pendências e volto
Então a importação continuou e a tela mostra o estado atual.

CA03 — Resumo ao concluir
Dado a importação concluída
Quando a tela atualiza
Então mostra horário de término e os totais: importado, ignorados fora de escopo, novas,
atualizadas e alertas (clicável para o log).

CA04 — Falha
Dado uma importação que falhou
Quando a tela atualiza
Então mostra "Importação não concluída", o motivo, e que nenhuma OS foi alterada (HU-004 CA06).

CA05 — Última importação
Dado nenhuma importação em andamento
Quando abro a tela
Então vejo os cartões "Última importação" (data/hora), "Registros processados" e "Divergências".

CA06 — Uma por vez
Dado uma importação do Polo 1 em andamento
Quando outro usuário tenta importar no Polo 1
Então o envio é bloqueado com "Já existe uma importação em andamento neste polo, iniciada por <nome> às <hora>".
