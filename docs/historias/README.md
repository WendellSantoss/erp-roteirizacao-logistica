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
ordem: 0                      # gerado pelo script — posição na ordem de desenvolvimento
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

## Ordem de desenvolvimento

Sequência em que as histórias devem ser implementadas. Nenhuma história aparece antes das
histórias de que depende; entre as que já podem começar, vem primeiro a de menor fase. O número
também está no campo `ordem` de cada história e no campo "Ordem" do GitHub Project.
Gerada por `python3 scripts/historias.py` a partir do `depende_de` — não editar à mão.

<!-- ordem:inicio -->

| Ordem | ID | Título | Fase | Depende de |
|---|---|---|---|---|
| 1 | [HU-F01](fundacao/HU-F01-montar-monorepo.md) | Montar o monorepo | 0 | — |
| 2 | [HU-F02](fundacao/HU-F02-ambiente-local-docker.md) | Subir o ambiente local com um comando | 0 | HU-F01 (1) |
| 3 | [HU-F03](fundacao/HU-F03-esqueleto-backend.md) | Criar o esqueleto do backend | 0 | HU-F02 (2) |
| 4 | [HU-F04](fundacao/HU-F04-esqueleto-frontend.md) | Criar o esqueleto do frontend | 0 | HU-F02 (2) |
| 5 | [HU-F05](fundacao/HU-F05-contrato-api.md) | Publicar o contrato da API | 0 | HU-F03 (3), HU-F04 (4) |
| 6 | [HU-F06](fundacao/HU-F06-integracao-continua.md) | Bloquear merge sem CI verde | 0 | HU-F03 (3), HU-F04 (4) |
| 7 | [HU-F07](fundacao/HU-F07-estrutura-specs.md) | Preparar o repositório para desenvolvimento por especificação | 0 | HU-F01 (1) |
| 8 | [HU-F08](fundacao/HU-F08-tarefas-assincronas.md) | Executar tarefas assíncronas com progresso | 0 | HU-F03 (3) |
| 9 | [HU-F09](fundacao/HU-F09-dados-de-exemplo.md) | Gerar dados de exemplo anonimizados | 0 | HU-F03 (3) |
| 10 | [HU-F10](fundacao/HU-F10-ambiente-de-homologacao.md) | Publicar ambiente de homologação | 0 | HU-F02 (2), HU-F06 (6) |
| 11 | [HU-F11](fundacao/HU-F11-ciclo-de-vida-da-os.md) | Modelar as entidades centrais e o ciclo de vida da OS | 0 | HU-F03 (3) |
| 12 | [HU-F12](fundacao/HU-F12-testes-ponta-a-ponta.md) | Rodar testes de ponta a ponta no navegador | 0 | HU-F04 (4), HU-F06 (6), HU-F09 (9) |
| 13 | [HU-F13](fundacao/HU-F13-disponibilidade-e-backup.md) | Monitorar a disponibilidade e garantir backup restaurável | 0 | HU-F10 (10) |
| 14 | [HU-019](HU-019-autenticacao-individual.md) | Entrar no sistema com usuário individual | 1 | HU-F03 (3), HU-F04 (4) |
| 15 | [HU-001](HU-001-upload-planilha-gsan.md) | Enviar a planilha diária do GSAN | 1 | HU-F04 (4), HU-F08 (8), HU-019 (14) |
| 16 | [HU-002](HU-002-validar-layout-da-planilha.md) | Validar o layout da planilha antes de importar | 1 | HU-001 (15) |
| 17 | [HU-021](HU-021-exibir-progresso-da-importacao.md) | Acompanhar o progresso da importação | 1 | HU-001 (15), HU-F08 (8) |
| 18 | [HU-020](HU-020-controlar-acesso-por-perfil.md) | Restringir módulos e ações pelo perfil do usuário | 1 | HU-019 (14) |
| 19 | [HU-045](HU-045-trilha-de-auditoria.md) | Manter a trilha de auditoria das alterações | 1 | HU-019 (14), HU-F03 (3) |
| 20 | [HU-054](HU-054-seletor-global-de-polo.md) | Escolher o polo de trabalho em qualquer tela | 1 | HU-020 (18), HU-F11 (11) |
| 21 | [HU-055](HU-055-confirmacao-visual-das-acoes.md) | Ver a confirmação de cada ação concluída | 1 | HU-F04 (4) |
| 22 | [HU-065](HU-065-gerenciar-usuarios-e-perfis.md) | Gerenciar usuários, perfis e polos de acesso | 1 | HU-019 (14), HU-020 (18) |
| 23 | [HU-066](HU-066-parametrizar-contrato.md) | Parametrizar preços, prazos, unidades do escopo e operações | 1 | HU-020 (18), HU-F11 (11) |
| 24 | [HU-003](HU-003-filtrar-oss-fora-de-escopo.md) | Descartar OSs fora do escopo contratual | 1 | HU-002 (16), HU-066 (23) |
| 25 | [HU-004](HU-004-atualizar-oss-sem-perder-tratamento.md) | Inserir e atualizar OSs sem perder o tratamento feito | 1 | HU-003 (24), HU-F11 (11) |
| 26 | [HU-005](HU-005-capturar-coordenadas-das-unidades.md) | Capturar as coordenadas das unidades no portal GSAN | 1 | HU-004 (25), HU-F08 (8) |
| 27 | [HU-006](HU-006-listar-oss-pendentes.md) | Listar as OSs que precisam de tratamento | 1 | HU-004 (25), HU-054 (20) |
| 28 | [HU-007](HU-007-exibir-colunas-das-oss.md) | Exibir as colunas operacionais da OS na lista de pendências | 1 | HU-006 (27) |
| 29 | [HU-008](HU-008-calcular-e-destacar-atraso.md) | Calcular e destacar o atraso de cada OS | 1 | HU-007 (28), HU-066 (23) |
| 30 | [HU-022](HU-022-exibir-progresso-da-captura.md) | Ver o progresso da captura no cabeçalho | 1 | HU-005 (26) |
| 31 | [HU-023](HU-023-reprocessar-falhas-de-captura.md) | Ver e reprocessar as unidades cuja captura falhou | 1 | HU-005 (26), HU-022 (30) |
| 32 | [HU-024](HU-024-preencher-coordenadas-manualmente.md) | Informar a coordenada de uma unidade manualmente | 1 | HU-023 (31) |
| 33 | [HU-025](HU-025-filtrar-oss-por-status.md) | Filtrar as pendências por situação com contador | 1 | HU-006 (27), HU-008 (29) |
| 34 | [HU-026](HU-026-desconsiderar-os.md) | Desconsiderar uma OS | 1 | HU-006 (27), HU-020 (18), HU-F11 (11) |
| 35 | [HU-046](HU-046-reaproveitar-coordenadas-capturadas.md) | Reaproveitar coordenadas já capturadas | 1 | HU-005 (26) |
| 36 | [HU-060](HU-060-concluir-tratamento-da-pendencia.md) | Liberar OSs tratadas para roteirização | 1 | HU-006 (27), HU-F11 (11) |
| 37 | [HU-011](HU-011-selecionar-operacao-e-data.md) | Escolher a operação e a data do planejamento | 2 | HU-054 (20), HU-066 (23) |
| 38 | [HU-012](HU-012-selecionar-oss-por-poligono.md) | Selecionar OSs por polígono no mapa | 2 | HU-005 (26), HU-011 (37), HU-060 (36) |
| 39 | [HU-028](HU-028-cadastrar-profissionais-e-ajudantes.md) | Cadastrar profissionais e ajudantes | 2 | HU-020 (18) |
| 40 | [HU-009](HU-009-cadastrar-equipes.md) | Cadastrar, editar e inativar equipes | 2 | HU-028 (39), HU-020 (18), HU-045 (19) |
| 41 | [HU-010](HU-010-vincular-equipe-ao-polo.md) | Restringir cada equipe ao seu polo | 2 | HU-009 (40) |
| 42 | [HU-027](HU-027-exibir-equipes-ativas.md) | Ver quantas equipes estão disponíveis no polo | 2 | HU-009 (40), HU-054 (20) |
| 43 | [HU-030](HU-030-alternar-lista-e-card.md) | Alternar entre visualização em lista e em cartões | 2 | HU-011 (37) |
| 44 | [HU-031](HU-031-contador-e-limpar-selecao.md) | Ver o contador de OSs selecionadas e limpar a seleção | 2 | HU-012 (38) |
| 45 | [HU-056](HU-056-criar-rota.md) | Criar rota a partir das OSs selecionadas | 2 | HU-009 (40), HU-012 (38), HU-028 (39) |
| 46 | [HU-029](HU-029-impedir-inativacao-com-rota-aberta.md) | Impedir a inativação de equipe com rota em aberto | 2 | HU-009 (40), HU-056 (45) |
| 47 | [HU-057](HU-057-atribuir-despacho.md) | Atribuir rapidamente as OSs selecionadas a uma equipe | 2 | HU-056 (45) |
| 48 | [HU-013](HU-013-finalizar-planejamento.md) | Finalizar o planejamento do dia | 2 | HU-056 (45), HU-057 (47) |
| 49 | [HU-014](HU-014-gerar-arquivo-rpa.md) | Gerar o arquivo de despacho para o RPA | 2 | HU-013 (48), HU-F11 (11) |
| 50 | [HU-058](HU-058-marcar-os-como-prioridade.md) | Marcar uma OS como prioridade | 2 | HU-012 (38) |
| 51 | [HU-059](HU-059-trocar-servico-ou-equipe.md) | Trocar a equipe ou retirar uma OS da rota antes do despacho | 2 | HU-056 (45) |
| 52 | [HU-037](HU-037-upload-planilha-de-execucao.md) | Enviar a planilha de execução do GSAN | 3 | HU-001 (15), HU-002 (16), HU-F08 (8) |
| 53 | [HU-018](HU-018-conciliar-execucao-com-despacho.md) | Conciliar a execução com as OSs despachadas | 3 | HU-037 (52), HU-014 (49), HU-F11 (11), HU-066 (23) |
| 54 | [HU-038](HU-038-grade-de-auditoria.md) | Ver a grade de auditoria da execução | 3 | HU-018 (53) |
| 55 | [HU-040](HU-040-registrar-alteracoes-da-auditoria.md) | Registrar cada correção feita na grade | 3 | HU-045 (19) |
| 56 | [HU-039](HU-039-editar-na-grade.md) | Corrigir dados da execução direto na grade | 3 | HU-038 (54), HU-040 (55) |
| 57 | [HU-041](HU-041-exibir-producao-bruta.md) | Ver a produção bruta do período | 3 | HU-018 (53), HU-054 (20) |
| 58 | [HU-042](HU-042-exibir-producao-validada.md) | Ver a produção validada e a taxa de conversão | 3 | HU-041 (57) |
| 59 | [HU-043](HU-043-calcular-glosa-potencial.md) | Ver o impacto financeiro da glosa potencial | 3 | HU-042 (58) |
| 60 | [HU-044](HU-044-previa-do-boletim-de-medicao.md) | Ver a prévia do Boletim de Medição do polo | 3 | HU-042 (58) |
| 61 | [HU-048](HU-048-funil-de-conversao-diario.md) | Ver o funil de conversão diário | 3 | HU-041 (57), HU-F11 (11) |
| 62 | [HU-061](HU-061-listar-invalidacoes.md) | Ver as OSs reprovadas pela fiscalização | 3 | HU-018 (53) |
| 63 | [HU-062](HU-062-forcar-validacao.md) | Forçar a validação de uma OS reprovada | 3 | HU-061 (62), HU-020 (18) |
| 64 | [HU-064](HU-064-fechar-e-reabrir-ciclo.md) | Fechar e reabrir o ciclo de medição | 3 | HU-044 (60), HU-F11 (11) |
| 65 | [HU-068](HU-068-ranking-de-equipes.md) | Ver o ranking de equipes | 3 | HU-042 (58) |
| 66 | [HU-032](HU-032-parametrizar-tipos-de-kit.md) | Manter o catálogo de tipos de kit | 4 | HU-020 (18) |
| 67 | [HU-015](HU-015-registrar-saida-de-kits.md) | Registrar a saída de kits para uma equipe | 4 | HU-009 (40), HU-032 (66), HU-054 (20) |
| 68 | [HU-016](HU-016-trava-de-historico.md) | Bloquear saída de kit acima da execução anterior | 4 | HU-015 (67), HU-018 (53), HU-066 (23) |
| 69 | [HU-033](HU-033-mensagem-de-bloqueio-da-saida.md) | Explicar por que a saída foi bloqueada | 4 | HU-016 (68) |
| 70 | [HU-034](HU-034-painel-execucao-dia-anterior.md) | Ver a execução de ontem por kit | 4 | HU-016 (68), HU-032 (66) |
| 71 | [HU-063](HU-063-liberar-trava-excepcionalmente.md) | Liberar excepcionalmente a trava de histórico | 4 | HU-016 (68), HU-033 (69) |
| 72 | [HU-067](HU-067-registrar-envio-entre-polos.md) | Registrar envio de kits para outro polo | 4 | HU-032 (66) |
| 73 | [HU-035](HU-035-listar-envios-pendentes.md) | Acompanhar os envios de kits para outros polos | 4 | HU-067 (72) |
| 74 | [HU-036](HU-036-listar-recebimentos-pendentes.md) | Ver as cargas a receber no meu polo | 4 | HU-067 (72) |
| 75 | [HU-017](HU-017-confirmar-recebimento-de-carga.md) | Confirmar o recebimento de uma carga | 4 | HU-036 (74) |
| 76 | [HU-047](HU-047-registrar-divergencia-no-recebimento.md) | Registrar divergência no recebimento | 4 | HU-017 (75) |
| 77 | [HU-049](HU-049-acessar-assistente.md) | Abrir o assistente de qualquer tela | 4 | HU-019 (14), HU-F04 (4) |
| 78 | [HU-050](HU-050-perguntar-em-linguagem-natural.md) | Perguntar sobre a operação em linguagem natural | 4 | HU-049 (77), HU-020 (18), HU-041 (57) |
| 79 | [HU-051](HU-051-respostas-estruturadas.md) | Receber respostas estruturadas, como o detalhe do BM | 4 | HU-050 (78), HU-044 (60) |
| 80 | [HU-053](HU-053-confirmar-acoes-do-assistente.md) | Confirmar antes que o assistente execute uma ação | 4 | HU-049 (77) |
| 81 | [HU-052](HU-052-sugestoes-acionaveis.md) | Executar operações a partir de sugestões do assistente | 4 | HU-050 (78), HU-053 (80), HU-057 (47) |

<!-- ordem:fim -->

## Índice por épico

> Gerado por `python3 scripts/historias.py` a partir dos cabeçalhos. Matriz de cobertura da ERS em [RASTREABILIDADE.md](RASTREABILIDADE.md).

<!-- indice:inicio -->

### EP-0 Fundação técnica (13)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 1 | [HU-F01](fundacao/HU-F01-montar-monorepo.md) | Montar o monorepo | 0 | MVP | rascunho | — | — |
| 2 | [HU-F02](fundacao/HU-F02-ambiente-local-docker.md) | Subir o ambiente local com um comando | 0 | MVP | rascunho | — | HU-F01 |
| 3 | [HU-F03](fundacao/HU-F03-esqueleto-backend.md) | Criar o esqueleto do backend | 0 | MVP | rascunho | — | HU-F02 |
| 4 | [HU-F04](fundacao/HU-F04-esqueleto-frontend.md) | Criar o esqueleto do frontend | 0 | MVP | rascunho | — | HU-F02 |
| 5 | [HU-F05](fundacao/HU-F05-contrato-api.md) | Publicar o contrato da API | 0 | MVP | rascunho | — | HU-F03, HU-F04 |
| 6 | [HU-F06](fundacao/HU-F06-integracao-continua.md) | Bloquear merge sem CI verde | 0 | MVP | rascunho | — | HU-F03, HU-F04 |
| 7 | [HU-F07](fundacao/HU-F07-estrutura-specs.md) | Preparar o repositório para desenvolvimento por especificação | 0 | MVP | rascunho | — | HU-F01 |
| 8 | [HU-F08](fundacao/HU-F08-tarefas-assincronas.md) | Executar tarefas assíncronas com progresso | 0 | MVP | rascunho | — | HU-F03 |
| 9 | [HU-F09](fundacao/HU-F09-dados-de-exemplo.md) | Gerar dados de exemplo anonimizados | 0 | MVP | rascunho | — | HU-F03 |
| 10 | [HU-F10](fundacao/HU-F10-ambiente-de-homologacao.md) | Publicar ambiente de homologação | 0 | MVP | rascunho | — | HU-F02, HU-F06 |
| 11 | [HU-F11](fundacao/HU-F11-ciclo-de-vida-da-os.md) | Modelar as entidades centrais e o ciclo de vida da OS | 0 | MVP | rascunho | — | HU-F03 |
| 12 | [HU-F12](fundacao/HU-F12-testes-ponta-a-ponta.md) | Rodar testes de ponta a ponta no navegador | 0 | MVP | rascunho | — | HU-F04, HU-F06, HU-F09 |
| 13 | [HU-F13](fundacao/HU-F13-disponibilidade-e-backup.md) | Monitorar a disponibilidade e garantir backup restaurável | 0 | MVP | rascunho | — | HU-F10 |

### EP-A Ingestão e preparação de dados (16)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 15 | [HU-001](HU-001-upload-planilha-gsan.md) | Enviar a planilha diária do GSAN | 1 | MVP | rascunho | RF-IMP-01 | HU-F04, HU-F08, HU-019 |
| 16 | [HU-002](HU-002-validar-layout-da-planilha.md) | Validar o layout da planilha antes de importar | 1 | MVP | rascunho | RF-IMP-02 | HU-001 |
| 24 | [HU-003](HU-003-filtrar-oss-fora-de-escopo.md) | Descartar OSs fora do escopo contratual | 1 | MVP | rascunho | RF-IMP-03 | HU-002, HU-066 |
| 25 | [HU-004](HU-004-atualizar-oss-sem-perder-tratamento.md) | Inserir e atualizar OSs sem perder o tratamento feito | 1 | MVP | rascunho | RF-IMP-04 | HU-003, HU-F11 |
| 26 | [HU-005](HU-005-capturar-coordenadas-das-unidades.md) | Capturar as coordenadas das unidades no portal GSAN | 1 | MVP | rascunho | RF-WEB-01 | HU-004, HU-F08 |
| 27 | [HU-006](HU-006-listar-oss-pendentes.md) | Listar as OSs que precisam de tratamento | 1 | MVP | rascunho | RF-PEN-01 | HU-004, HU-054 |
| 28 | [HU-007](HU-007-exibir-colunas-das-oss.md) | Exibir as colunas operacionais da OS na lista de pendências | 1 | MVP | rascunho | RF-PEN-03 | HU-006 |
| 29 | [HU-008](HU-008-calcular-e-destacar-atraso.md) | Calcular e destacar o atraso de cada OS | 1 | MVP | rascunho | RF-PEN-04 | HU-007, HU-066 |
| 17 | [HU-021](HU-021-exibir-progresso-da-importacao.md) | Acompanhar o progresso da importação | 1 | MVP | rascunho | RF-IMP-05 | HU-001, HU-F08 |
| 30 | [HU-022](HU-022-exibir-progresso-da-captura.md) | Ver o progresso da captura no cabeçalho | 1 | MVP | rascunho | RF-WEB-02 | HU-005 |
| 31 | [HU-023](HU-023-reprocessar-falhas-de-captura.md) | Ver e reprocessar as unidades cuja captura falhou | 1 | MVP | rascunho | RF-WEB-03 | HU-005, HU-022 |
| 32 | [HU-024](HU-024-preencher-coordenadas-manualmente.md) | Informar a coordenada de uma unidade manualmente | 1 | MVP | rascunho | RF-WEB-04 | HU-023 |
| 33 | [HU-025](HU-025-filtrar-oss-por-status.md) | Filtrar as pendências por situação com contador | 1 | MVP | rascunho | RF-PEN-02 | HU-006, HU-008 |
| 34 | [HU-026](HU-026-desconsiderar-os.md) | Desconsiderar uma OS | 1 | MVP | rascunho | RF-PEN-05 | HU-006, HU-020, HU-F11 |
| 35 | [HU-046](HU-046-reaproveitar-coordenadas-capturadas.md) | Reaproveitar coordenadas já capturadas | 1 | MVP | rascunho | RF-WEB-05 | HU-005 |
| 36 | [HU-060](HU-060-concluir-tratamento-da-pendencia.md) | Liberar OSs tratadas para roteirização | 1 | MVP | proposta | RF-PEN-06 (proposto) | HU-006, HU-F11 |

### EP-B Planejamento e despacho (15)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 40 | [HU-009](HU-009-cadastrar-equipes.md) | Cadastrar, editar e inativar equipes | 2 | MVP | rascunho | RF-EQP-01 | HU-028, HU-020, HU-045 |
| 41 | [HU-010](HU-010-vincular-equipe-ao-polo.md) | Restringir cada equipe ao seu polo | 2 | MVP | rascunho | RF-EQP-03 | HU-009 |
| 37 | [HU-011](HU-011-selecionar-operacao-e-data.md) | Escolher a operação e a data do planejamento | 2 | MVP | rascunho | RF-ROT-01 | HU-054, HU-066 |
| 38 | [HU-012](HU-012-selecionar-oss-por-poligono.md) | Selecionar OSs por polígono no mapa | 2 | MVP | rascunho | RF-ROT-07 | HU-005, HU-011, HU-060 |
| 48 | [HU-013](HU-013-finalizar-planejamento.md) | Finalizar o planejamento do dia | 2 | MVP | rascunho | RF-ROT-16 | HU-056, HU-057 |
| 49 | [HU-014](HU-014-gerar-arquivo-rpa.md) | Gerar o arquivo de despacho para o RPA | 2 | MVP | rascunho | RF-ROT-17 | HU-013, HU-F11 |
| 42 | [HU-027](HU-027-exibir-equipes-ativas.md) | Ver quantas equipes estão disponíveis no polo | 2 | MVP | rascunho | RF-EQP-02 | HU-009, HU-054 |
| 39 | [HU-028](HU-028-cadastrar-profissionais-e-ajudantes.md) | Cadastrar profissionais e ajudantes | 2 | MVP | rascunho | RF-EQP-04 | HU-020 |
| 46 | [HU-029](HU-029-impedir-inativacao-com-rota-aberta.md) | Impedir a inativação de equipe com rota em aberto | 2 | MVP | rascunho | RF-EQP-05 | HU-009, HU-056 |
| 43 | [HU-030](HU-030-alternar-lista-e-card.md) | Alternar entre visualização em lista e em cartões | 2 | MVP | rascunho | RF-ROT-02 | HU-011 |
| 44 | [HU-031](HU-031-contador-e-limpar-selecao.md) | Ver o contador de OSs selecionadas e limpar a seleção | 2 | MVP | rascunho | RF-ROT-08 | HU-012 |
| 45 | [HU-056](HU-056-criar-rota.md) | Criar rota a partir das OSs selecionadas | 2 | MVP | proposta | RF-ROT-03 (proposto) | HU-009, HU-012, HU-028 |
| 47 | [HU-057](HU-057-atribuir-despacho.md) | Atribuir rapidamente as OSs selecionadas a uma equipe | 2 | MVP | proposta | RF-ROT-04 (proposto) | HU-056 |
| 50 | [HU-058](HU-058-marcar-os-como-prioridade.md) | Marcar uma OS como prioridade | 2 | MVP | proposta | RF-ROT-05 (proposto) | HU-012 |
| 51 | [HU-059](HU-059-trocar-servico-ou-equipe.md) | Trocar a equipe ou retirar uma OS da rota antes do despacho | 2 | MVP | proposta | RF-ROT-06 (proposto) | HU-056 |

### EP-C Suprimentos e logística (11)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 67 | [HU-015](HU-015-registrar-saida-de-kits.md) | Registrar a saída de kits para uma equipe | 4 | MVP | rascunho | RF-ALM-01 | HU-009, HU-032, HU-054 |
| 68 | [HU-016](HU-016-trava-de-historico.md) | Bloquear saída de kit acima da execução anterior | 4 | MVP | rascunho | RF-ALM-03, RF-ALM-04 | HU-015, HU-018, HU-066 |
| 75 | [HU-017](HU-017-confirmar-recebimento-de-carga.md) | Confirmar o recebimento de uma carga | 4 | MVP | rascunho | RF-ALM-09 | HU-036 |
| 66 | [HU-032](HU-032-parametrizar-tipos-de-kit.md) | Manter o catálogo de tipos de kit | 4 | MVP | rascunho | RF-ALM-02 | HU-020 |
| 69 | [HU-033](HU-033-mensagem-de-bloqueio-da-saida.md) | Explicar por que a saída foi bloqueada | 4 | MVP | rascunho | RF-ALM-04 | HU-016 |
| 70 | [HU-034](HU-034-painel-execucao-dia-anterior.md) | Ver a execução de ontem por kit | 4 | MVP | rascunho | RF-ALM-05 | HU-016, HU-032 |
| 73 | [HU-035](HU-035-listar-envios-pendentes.md) | Acompanhar os envios de kits para outros polos | 4 | MVP | rascunho | RF-ALM-07 | HU-067 |
| 74 | [HU-036](HU-036-listar-recebimentos-pendentes.md) | Ver as cargas a receber no meu polo | 4 | MVP | rascunho | RF-ALM-08 | HU-067 |
| 76 | [HU-047](HU-047-registrar-divergencia-no-recebimento.md) | Registrar divergência no recebimento | 4 | desejável | rascunho | RF-ALM-10 | HU-017 |
| 71 | [HU-063](HU-063-liberar-trava-excepcionalmente.md) | Liberar excepcionalmente a trava de histórico | 4 | MVP | proposta | RF-ALM-06 (proposto) | HU-016, HU-033 |
| 72 | [HU-067](HU-067-registrar-envio-entre-polos.md) | Registrar envio de kits para outro polo | 4 | MVP | proposta | RF-ALM-11 (proposto) | HU-032 |

### EP-D Fechamento, auditoria e faturamento (14)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 53 | [HU-018](HU-018-conciliar-execucao-com-despacho.md) | Conciliar a execução com as OSs despachadas | 3 | MVP | rascunho | RF-AUD-02 | HU-037, HU-014, HU-F11, HU-066 |
| 52 | [HU-037](HU-037-upload-planilha-de-execucao.md) | Enviar a planilha de execução do GSAN | 3 | MVP | rascunho | RF-AUD-01 | HU-001, HU-002, HU-F08 |
| 54 | [HU-038](HU-038-grade-de-auditoria.md) | Ver a grade de auditoria da execução | 3 | MVP | rascunho | RF-AUD-03 | HU-018 |
| 56 | [HU-039](HU-039-editar-na-grade.md) | Corrigir dados da execução direto na grade | 3 | MVP | rascunho | RF-AUD-04 | HU-038, HU-040 |
| 55 | [HU-040](HU-040-registrar-alteracoes-da-auditoria.md) | Registrar cada correção feita na grade | 3 | MVP | rascunho | RF-AUD-05 | HU-045 |
| 57 | [HU-041](HU-041-exibir-producao-bruta.md) | Ver a produção bruta do período | 3 | MVP | rascunho | RF-GER-01 | HU-018, HU-054 |
| 58 | [HU-042](HU-042-exibir-producao-validada.md) | Ver a produção validada e a taxa de conversão | 3 | MVP | rascunho | RF-GER-02 | HU-041 |
| 59 | [HU-043](HU-043-calcular-glosa-potencial.md) | Ver o impacto financeiro da glosa potencial | 3 | MVP | rascunho | RF-GER-03 | HU-042 |
| 60 | [HU-044](HU-044-previa-do-boletim-de-medicao.md) | Ver a prévia do Boletim de Medição do polo | 3 | MVP | rascunho | RF-GER-04 | HU-042 |
| 61 | [HU-048](HU-048-funil-de-conversao-diario.md) | Ver o funil de conversão diário | 3 | MVP | rascunho | RF-GER-05 | HU-041, HU-F11 |
| 62 | [HU-061](HU-061-listar-invalidacoes.md) | Ver as OSs reprovadas pela fiscalização | 3 | MVP | proposta | RF-AUD-06 (proposto) | HU-018 |
| 63 | [HU-062](HU-062-forcar-validacao.md) | Forçar a validação de uma OS reprovada | 3 | MVP | proposta | RF-AUD-07 (proposto) | HU-061, HU-020 |
| 64 | [HU-064](HU-064-fechar-e-reabrir-ciclo.md) | Fechar e reabrir o ciclo de medição | 3 | MVP | proposta | RF-AUD-08 (proposto) | HU-044, HU-F11 |
| 65 | [HU-068](HU-068-ranking-de-equipes.md) | Ver o ranking de equipes | 3 | desejável | proposta | RF-GER-06 (proposto) | HU-042 |

### EP-E Inteligência e suporte à decisão (5)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 77 | [HU-049](HU-049-acessar-assistente.md) | Abrir o assistente de qualquer tela | 4 | MVP | rascunho | RF-ASS-01 | HU-019, HU-F04 |
| 78 | [HU-050](HU-050-perguntar-em-linguagem-natural.md) | Perguntar sobre a operação em linguagem natural | 4 | MVP | rascunho | RF-ASS-02 | HU-049, HU-020, HU-041 |
| 79 | [HU-051](HU-051-respostas-estruturadas.md) | Receber respostas estruturadas, como o detalhe do BM | 4 | MVP | rascunho | RF-ASS-03 | HU-050, HU-044 |
| 81 | [HU-052](HU-052-sugestoes-acionaveis.md) | Executar operações a partir de sugestões do assistente | 4 | MVP | rascunho | RF-ASS-04 | HU-050, HU-053, HU-057 |
| 80 | [HU-053](HU-053-confirmar-acoes-do-assistente.md) | Confirmar antes que o assistente execute uma ação | 4 | MVP | rascunho | RF-ASS-05 | HU-049 |

### EP-F Requisitos transversais (7)

| Ordem | ID | Título | Fase | Prioridade | Status | Requisitos | Depende de |
|---|---|---|---|---|---|---|---|
| 14 | [HU-019](HU-019-autenticacao-individual.md) | Entrar no sistema com usuário individual | 1 | MVP | rascunho | RF-TRV-01 | HU-F03, HU-F04 |
| 18 | [HU-020](HU-020-controlar-acesso-por-perfil.md) | Restringir módulos e ações pelo perfil do usuário | 1 | MVP | rascunho | RF-TRV-02 | HU-019 |
| 19 | [HU-045](HU-045-trilha-de-auditoria.md) | Manter a trilha de auditoria das alterações | 1 | MVP | rascunho | RF-TRV-04 | HU-019, HU-F03 |
| 20 | [HU-054](HU-054-seletor-global-de-polo.md) | Escolher o polo de trabalho em qualquer tela | 1 | MVP | rascunho | RF-TRV-03 | HU-020, HU-F11 |
| 21 | [HU-055](HU-055-confirmacao-visual-das-acoes.md) | Ver a confirmação de cada ação concluída | 1 | MVP | rascunho | RF-TRV-05 | HU-F04 |
| 22 | [HU-065](HU-065-gerenciar-usuarios-e-perfis.md) | Gerenciar usuários, perfis e polos de acesso | 1 | MVP | proposta | RF-TRV-06 (proposto) | HU-019, HU-020 |
| 23 | [HU-066](HU-066-parametrizar-contrato.md) | Parametrizar preços, prazos, unidades do escopo e operações | 1 | MVP | proposta | RF-TRV-07 (proposto) | HU-020, HU-F11 |

<!-- indice:fim -->
