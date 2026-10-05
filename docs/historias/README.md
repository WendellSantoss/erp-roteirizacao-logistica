# Histórias de usuário do GeniOS

Cada história é um arquivo `.md` nesta pasta. O arquivo é a fonte da verdade; a issue no GitHub
Project aponta para ele. Como o desenvolvimento é feito com agentes de IA a partir de
especificações, a história precisa ser precisa o bastante para que **duas pessoas (ou dois
agentes) implementem a mesma coisa** a partir dela.

## Numeração

| Faixa | O que é |
|---|---|
| `HU-F01` … `HU-F12` | Fundação técnica: repositório, ambiente, CI, esqueletos, ciclo de vida da OS, testes E2E. Vêm antes de tudo. Ficam em `fundacao/`. |
| `HU-001` … `HU-055` | Histórias originais do Project, reescritas. A numeração foi mantida para preservar o vínculo com as issues. |
| `HU-056` em diante | Histórias novas que cobrem lacunas da ERS (ver `docs/requisitos/lacunas.md`). Nascem com `status: proposta`. |

## Modelo

```markdown
---
id: HU-000
titulo: Verbo no infinitivo + objeto
epico: EP-A Ingestão e preparação de dados   # ver Índice
tela: nome da tela no protótipo (docs/design/prototipo/GeniOS ERP.html)
modulo: Importação | Webscraper | Pendências | Equipes | Roteirizador | Almoxarifado | Auditoria | Gerencial | Assistente | Transversal | Fundação
fase: 0 (fundação) | 1 | 2 | 3 | 4   # faseamento da ERS §8
prioridade: MVP | desejável
status: proposta | rascunho | pronta | em desenvolvimento | concluída
requisitos: [RF-XXX-00]        # RFs da ERS que a história cumpre
regras: [RN-00]                # regras de negócio que se aplicam
nao_funcionais: [RNF-00]       # RNFs verificados por esta história
depende_de: [HU-000]           # histórias que precisam estar concluídas antes
---

# HU-000 — Título

## História
Como **perfil da ERS**, quero **capacidade**, para **resultado de negócio**.

## Contexto
O que já existe, de onde vêm os dados, onde a história entra no ciclo de vida da OS.

## Regras de negócio
Regras da ERS citadas pelo número, mais as regras específicas desta história (RN-L01, RN-L02…).

## Critérios de aceite
CA01 — nome curto (caminho feliz)
Dado …
Quando …
Então …

CA02 — nome curto (erro / borda)
…

## Fora de escopo
O que esta história explicitamente não faz e qual história faz.

## Dúvidas em aberto
Perguntas que bloqueiam o status "pronta".
```

## Regras de escrita

- **Critério de aceite tem resultado observável.** "O sistema deve validar o arquivo" não é
  critério; "o arquivo é recusado com a mensagem *X* e nenhuma OS é gravada" é.
- **Números, não adjetivos.** "Rápido" vira "em até 2 s com 50.000 OSs".
- **Pelo menos um caminho de erro ou borda** por história, além do caminho feliz.
- **Permissão e polo** aparecem nos critérios sempre que a ação depende de perfil (RF-TRV-02) ou
  do seletor de polo (RF-TRV-03).
- **Regra da ERS é citada pelo número**, não reescrita com outras palavras — evita duas versões
  da mesma regra.
- **Uma história, um resultado de negócio.** Se tem "e" no título, provavelmente são duas.

## Definição de Pronta (pode ir para desenvolvimento)

- [ ] Todos os campos do cabeçalho preenchidos.
- [ ] Todo critério de aceite tem Dado / Quando / Então e resultado observável.
- [ ] Há ao menos um critério de erro ou borda.
- [ ] Nenhuma dúvida em aberto que mude o comportamento.
- [ ] Dependências estão concluídas ou planejadas antes.

## Definição de Concluída

- [ ] Cada critério de aceite tem pelo menos um teste automatizado com o ID no nome (ex.:
      `test_hu016_ca02_bloqueia_acima_da_execucao`).
- [ ] CI verde no pull request.
- [ ] Pull request revisado por outra pessoa do grupo.
- [ ] Status da história e da issue atualizados.

## Índice

> Gerado por `python3 scripts/historias.py` a partir dos cabeçalhos. Matriz de cobertura da ERS em [RASTREABILIDADE.md](RASTREABILIDADE.md).

<!-- indice:inicio -->

### EP-0 Fundação técnica (13)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-F01](fundacao/HU-F01-montar-monorepo.md) | Montar o monorepo | 0 | MVP | rascunho | — | — |
| [HU-F02](fundacao/HU-F02-ambiente-local-docker.md) | Subir o ambiente local com um comando | 0 | MVP | rascunho | — | HU-F01 |
| [HU-F03](fundacao/HU-F03-esqueleto-backend.md) | Criar o esqueleto do backend | 0 | MVP | rascunho | — | HU-F02 |
| [HU-F04](fundacao/HU-F04-esqueleto-frontend.md) | Criar o esqueleto do frontend | 0 | MVP | rascunho | — | HU-F02 |
| [HU-F05](fundacao/HU-F05-contrato-api.md) | Publicar o contrato da API | 0 | MVP | rascunho | — | HU-F03, HU-F04 |
| [HU-F06](fundacao/HU-F06-integracao-continua.md) | Bloquear merge sem CI verde | 0 | MVP | rascunho | — | HU-F03, HU-F04 |
| [HU-F07](fundacao/HU-F07-estrutura-specs.md) | Preparar o repositório para desenvolvimento por especificação | 0 | MVP | rascunho | — | HU-F01 |
| [HU-F08](fundacao/HU-F08-tarefas-assincronas.md) | Executar tarefas assíncronas com progresso | 0 | MVP | rascunho | — | HU-F03 |
| [HU-F09](fundacao/HU-F09-dados-de-exemplo.md) | Gerar dados de exemplo anonimizados | 0 | MVP | rascunho | — | HU-F03 |
| [HU-F10](fundacao/HU-F10-ambiente-de-homologacao.md) | Publicar ambiente de homologação | 0 | MVP | rascunho | — | HU-F02, HU-F06 |
| [HU-F11](fundacao/HU-F11-ciclo-de-vida-da-os.md) | Modelar as entidades centrais e o ciclo de vida da OS | 0 | MVP | rascunho | — | HU-F03 |
| [HU-F12](fundacao/HU-F12-testes-ponta-a-ponta.md) | Rodar testes de ponta a ponta no navegador | 0 | MVP | rascunho | — | HU-F04, HU-F06, HU-F09 |
| [HU-F13](fundacao/HU-F13-disponibilidade-e-backup.md) | Monitorar a disponibilidade e garantir backup restaurável | 0 | MVP | rascunho | — | HU-F10 |

### EP-A Ingestão e preparação de dados (16)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-001](HU-001-upload-planilha-gsan.md) | Enviar a planilha diária do GSAN | 1 | MVP | rascunho | RF-IMP-01 | HU-F04, HU-F08, HU-019 |
| [HU-002](HU-002-validar-layout-da-planilha.md) | Validar o layout da planilha antes de importar | 1 | MVP | rascunho | RF-IMP-02 | HU-001 |
| [HU-003](HU-003-filtrar-oss-fora-de-escopo.md) | Descartar OSs fora do escopo contratual | 1 | MVP | rascunho | RF-IMP-03 | HU-002, HU-066 |
| [HU-004](HU-004-atualizar-oss-sem-perder-tratamento.md) | Inserir e atualizar OSs sem perder o tratamento feito | 1 | MVP | rascunho | RF-IMP-04 | HU-003, HU-F11 |
| [HU-005](HU-005-capturar-coordenadas-das-unidades.md) | Capturar as coordenadas das unidades no portal GSAN | 1 | MVP | rascunho | RF-WEB-01 | HU-004, HU-F08 |
| [HU-006](HU-006-listar-oss-pendentes.md) | Listar as OSs que precisam de tratamento | 1 | MVP | rascunho | RF-PEN-01 | HU-004, HU-054 |
| [HU-007](HU-007-exibir-colunas-das-oss.md) | Exibir as colunas operacionais da OS na lista de pendências | 1 | MVP | rascunho | RF-PEN-03 | HU-006 |
| [HU-008](HU-008-calcular-e-destacar-atraso.md) | Calcular e destacar o atraso de cada OS | 1 | MVP | rascunho | RF-PEN-04 | HU-007, HU-066 |
| [HU-021](HU-021-exibir-progresso-da-importacao.md) | Acompanhar o progresso da importação | 1 | MVP | rascunho | RF-IMP-05 | HU-001, HU-F08 |
| [HU-022](HU-022-exibir-progresso-da-captura.md) | Ver o progresso da captura no cabeçalho | 1 | MVP | rascunho | RF-WEB-02 | HU-005 |
| [HU-023](HU-023-reprocessar-falhas-de-captura.md) | Ver e reprocessar as unidades cuja captura falhou | 1 | MVP | rascunho | RF-WEB-03 | HU-005, HU-022 |
| [HU-024](HU-024-preencher-coordenadas-manualmente.md) | Informar a coordenada de uma unidade manualmente | 1 | MVP | rascunho | RF-WEB-04 | HU-023 |
| [HU-025](HU-025-filtrar-oss-por-status.md) | Filtrar as pendências por situação com contador | 1 | MVP | rascunho | RF-PEN-02 | HU-006, HU-008 |
| [HU-026](HU-026-desconsiderar-os.md) | Desconsiderar uma OS | 1 | MVP | rascunho | RF-PEN-05 | HU-006, HU-020, HU-F11 |
| [HU-046](HU-046-reaproveitar-coordenadas-capturadas.md) | Reaproveitar coordenadas já capturadas | 1 | MVP | rascunho | RF-WEB-05 | HU-005 |
| [HU-060](HU-060-concluir-tratamento-da-pendencia.md) | Liberar OSs tratadas para roteirização | 1 | MVP | proposta | RF-PEN-06 (proposto) | HU-006, HU-F11 |

### EP-B Planejamento e despacho (15)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-009](HU-009-cadastrar-equipes.md) | Cadastrar, editar e inativar equipes | 2 | MVP | rascunho | RF-EQP-01 | HU-028, HU-020, HU-045 |
| [HU-010](HU-010-vincular-equipe-ao-polo.md) | Restringir cada equipe ao seu polo | 2 | MVP | rascunho | RF-EQP-03 | HU-009 |
| [HU-011](HU-011-selecionar-operacao-e-data.md) | Escolher a operação e a data do planejamento | 2 | MVP | rascunho | RF-ROT-01 | HU-054, HU-066 |
| [HU-012](HU-012-selecionar-oss-por-poligono.md) | Selecionar OSs por polígono no mapa | 2 | MVP | rascunho | RF-ROT-07 | HU-005, HU-011, HU-060 |
| [HU-013](HU-013-finalizar-planejamento.md) | Finalizar o planejamento do dia | 2 | MVP | rascunho | RF-ROT-16 | HU-056, HU-057 |
| [HU-014](HU-014-gerar-arquivo-rpa.md) | Gerar o arquivo de despacho para o RPA | 2 | MVP | rascunho | RF-ROT-17 | HU-013, HU-F11 |
| [HU-027](HU-027-exibir-equipes-ativas.md) | Ver quantas equipes estão disponíveis no polo | 2 | MVP | rascunho | RF-EQP-02 | HU-009, HU-054 |
| [HU-028](HU-028-cadastrar-profissionais-e-ajudantes.md) | Cadastrar profissionais e ajudantes | 2 | MVP | rascunho | RF-EQP-04 | HU-020 |
| [HU-029](HU-029-impedir-inativacao-com-rota-aberta.md) | Impedir a inativação de equipe com rota em aberto | 2 | MVP | rascunho | RF-EQP-05 | HU-009, HU-056 |
| [HU-030](HU-030-alternar-lista-e-card.md) | Alternar entre visualização em lista e em cartões | 2 | MVP | rascunho | RF-ROT-02 | HU-011 |
| [HU-031](HU-031-contador-e-limpar-selecao.md) | Ver o contador de OSs selecionadas e limpar a seleção | 2 | MVP | rascunho | RF-ROT-08 | HU-012 |
| [HU-056](HU-056-criar-rota.md) | Criar rota a partir das OSs selecionadas | 2 | MVP | proposta | RF-ROT-03 (proposto) | HU-009, HU-012, HU-028 |
| [HU-057](HU-057-atribuir-despacho.md) | Atribuir rapidamente as OSs selecionadas a uma equipe | 2 | MVP | proposta | RF-ROT-04 (proposto) | HU-056 |
| [HU-058](HU-058-marcar-os-como-prioridade.md) | Marcar uma OS como prioridade | 2 | MVP | proposta | RF-ROT-05 (proposto) | HU-012 |
| [HU-059](HU-059-trocar-servico-ou-equipe.md) | Trocar a equipe ou retirar uma OS da rota antes do despacho | 2 | MVP | proposta | RF-ROT-06 (proposto) | HU-056 |

### EP-C Suprimentos e logística (11)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-015](HU-015-registrar-saida-de-kits.md) | Registrar a saída de kits para uma equipe | 4 | MVP | rascunho | RF-ALM-01 | HU-009, HU-032, HU-054 |
| [HU-016](HU-016-trava-de-historico.md) | Bloquear saída de kit acima da execução anterior | 4 | MVP | rascunho | RF-ALM-03, RF-ALM-04 | HU-015, HU-018, HU-066 |
| [HU-017](HU-017-confirmar-recebimento-de-carga.md) | Confirmar o recebimento de uma carga | 4 | MVP | rascunho | RF-ALM-09 | HU-036 |
| [HU-032](HU-032-parametrizar-tipos-de-kit.md) | Manter o catálogo de tipos de kit | 4 | MVP | rascunho | RF-ALM-02 | HU-020 |
| [HU-033](HU-033-mensagem-de-bloqueio-da-saida.md) | Explicar por que a saída foi bloqueada | 4 | MVP | rascunho | RF-ALM-04 | HU-016 |
| [HU-034](HU-034-painel-execucao-dia-anterior.md) | Ver a execução de ontem por kit | 4 | MVP | rascunho | RF-ALM-05 | HU-016, HU-032 |
| [HU-035](HU-035-listar-envios-pendentes.md) | Acompanhar os envios de kits para outros polos | 4 | MVP | rascunho | RF-ALM-07 | HU-067 |
| [HU-036](HU-036-listar-recebimentos-pendentes.md) | Ver as cargas a receber no meu polo | 4 | MVP | rascunho | RF-ALM-08 | HU-067 |
| [HU-047](HU-047-registrar-divergencia-no-recebimento.md) | Registrar divergência no recebimento | 4 | desejável | rascunho | RF-ALM-10 | HU-017 |
| [HU-063](HU-063-liberar-trava-excepcionalmente.md) | Liberar excepcionalmente a trava de histórico | 4 | MVP | proposta | RF-ALM-06 (proposto) | HU-016, HU-033 |
| [HU-067](HU-067-registrar-envio-entre-polos.md) | Registrar envio de kits para outro polo | 4 | MVP | proposta | RF-ALM-11 (proposto) | HU-032 |

### EP-D Fechamento, auditoria e faturamento (14)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-018](HU-018-conciliar-execucao-com-despacho.md) | Conciliar a execução com as OSs despachadas | 3 | MVP | rascunho | RF-AUD-02 | HU-037, HU-014, HU-F11, HU-066 |
| [HU-037](HU-037-upload-planilha-de-execucao.md) | Enviar a planilha de execução do GSAN | 3 | MVP | rascunho | RF-AUD-01 | HU-001, HU-002, HU-F08 |
| [HU-038](HU-038-grade-de-auditoria.md) | Ver a grade de auditoria da execução | 3 | MVP | rascunho | RF-AUD-03 | HU-018 |
| [HU-039](HU-039-editar-na-grade.md) | Corrigir dados da execução direto na grade | 3 | MVP | rascunho | RF-AUD-04 | HU-038, HU-040 |
| [HU-040](HU-040-registrar-alteracoes-da-auditoria.md) | Registrar cada correção feita na grade | 3 | MVP | rascunho | RF-AUD-05 | HU-045 |
| [HU-041](HU-041-exibir-producao-bruta.md) | Ver a produção bruta do período | 3 | MVP | rascunho | RF-GER-01 | HU-018, HU-054 |
| [HU-042](HU-042-exibir-producao-validada.md) | Ver a produção validada e a taxa de conversão | 3 | MVP | rascunho | RF-GER-02 | HU-041 |
| [HU-043](HU-043-calcular-glosa-potencial.md) | Ver o impacto financeiro da glosa potencial | 3 | MVP | rascunho | RF-GER-03 | HU-042 |
| [HU-044](HU-044-previa-do-boletim-de-medicao.md) | Ver a prévia do Boletim de Medição do polo | 3 | MVP | rascunho | RF-GER-04 | HU-042 |
| [HU-048](HU-048-funil-de-conversao-diario.md) | Ver o funil de conversão diário | 3 | MVP | rascunho | RF-GER-05 | HU-041, HU-F11 |
| [HU-061](HU-061-listar-invalidacoes.md) | Ver as OSs reprovadas pela fiscalização | 3 | MVP | proposta | RF-AUD-06 (proposto) | HU-018 |
| [HU-062](HU-062-forcar-validacao.md) | Forçar a validação de uma OS reprovada | 3 | MVP | proposta | RF-AUD-07 (proposto) | HU-061, HU-020 |
| [HU-064](HU-064-fechar-e-reabrir-ciclo.md) | Fechar e reabrir o ciclo de medição | 3 | MVP | proposta | RF-AUD-08 (proposto) | HU-044, HU-F11 |
| [HU-068](HU-068-ranking-de-equipes.md) | Ver o ranking de equipes | 3 | desejável | proposta | RF-GER-06 (proposto) | HU-042 |

### EP-E Inteligência e suporte à decisão (5)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-049](HU-049-acessar-assistente.md) | Abrir o assistente de qualquer tela | 4 | MVP | rascunho | RF-ASS-01 | HU-019, HU-F04 |
| [HU-050](HU-050-perguntar-em-linguagem-natural.md) | Perguntar sobre a operação em linguagem natural | 4 | MVP | rascunho | RF-ASS-02 | HU-049, HU-020, HU-041 |
| [HU-051](HU-051-respostas-estruturadas.md) | Receber respostas estruturadas, como o detalhe do BM | 4 | MVP | rascunho | RF-ASS-03 | HU-050, HU-044 |
| [HU-052](HU-052-sugestoes-acionaveis.md) | Executar operações a partir de sugestões do assistente | 4 | MVP | rascunho | RF-ASS-04 | HU-050, HU-053, HU-057 |
| [HU-053](HU-053-confirmar-acoes-do-assistente.md) | Confirmar antes que o assistente execute uma ação | 4 | MVP | rascunho | RF-ASS-05 | HU-049 |

### EP-F Requisitos transversais (7)

| ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|
| [HU-019](HU-019-autenticacao-individual.md) | Entrar no sistema com usuário individual | 1 | MVP | rascunho | RF-TRV-01 | HU-F03, HU-F04 |
| [HU-020](HU-020-controlar-acesso-por-perfil.md) | Restringir módulos e ações pelo perfil do usuário | 1 | MVP | rascunho | RF-TRV-02 | HU-019 |
| [HU-045](HU-045-trilha-de-auditoria.md) | Manter a trilha de auditoria das alterações | 1 | MVP | rascunho | RF-TRV-04 | HU-019, HU-F03 |
| [HU-054](HU-054-seletor-global-de-polo.md) | Escolher o polo de trabalho em qualquer tela | 1 | MVP | rascunho | RF-TRV-03 | HU-020, HU-F11 |
| [HU-055](HU-055-confirmacao-visual-das-acoes.md) | Ver a confirmação de cada ação concluída | 1 | MVP | rascunho | RF-TRV-05 | HU-F04 |
| [HU-065](HU-065-gerenciar-usuarios-e-perfis.md) | Gerenciar usuários, perfis e polos de acesso | 1 | MVP | proposta | RF-TRV-06 (proposto) | HU-019, HU-020 |
| [HU-066](HU-066-parametrizar-contrato.md) | Parametrizar preços, prazos, unidades do escopo e operações | 1 | MVP | proposta | RF-TRV-07 (proposto) | HU-020, HU-F11 |

<!-- indice:fim -->
