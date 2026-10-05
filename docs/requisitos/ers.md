# **GeniOS**

Especificação de Requisitos de Software (ERS)

*ERP Operacional de Serviços de Campo*

*Ana Beatriz da Silva*

*Deivisson da Silva Rocha*

*Felipe de Almeida Silva*

*Wendell dos Santos*

# **1\. Introdução**

## **1.1 Objetivo**

Este documento especifica os requisitos funcionais e não funcionais do GeniOS, ERP operacional destinado à gestão do ciclo de vida completo de Ordens de Serviço (OS) de campo em contratos de saneamento. Serve como referência contratual entre a área de negócio e a equipe de desenvolvimento, e como base para os planos de teste e homologação.

## **1.2 Escopo do produto**

O GeniOS cobre a cadeia operacional desde a ingestão diária dos dados do GSAN até o fechamento financeiro da medição (BM). Está no escopo: importação e higienização de OSs, tratamento de pendências, roteirização e despacho de equipes, controle de kits do almoxarifado, auditoria da execução com confronto contra a fiscalização da concessionária, indicadores gerenciais e um assistente conversacional operacional.

Está fora do escopo desta versão: o aplicativo de campo utilizado pelas equipes, a emissão fiscal de notas, a folha de pagamento e a gestão de frota (manutenção de veículos).

## **1.3 Definições, acrônimos e siglas**

| Termo | Definição |
| :---- | :---- |
| OS | Ordem de Serviço — unidade elementar de trabalho executada em campo. |
| GSAN | Sistema de gestão comercial da concessionária, origem das OSs e destino da execução. |
| Upsert | Operação que insere o registro se novo e atualiza se já existente, preservando o histórico. |
| BM | Boletim de Medição — apuração periódica dos serviços executados e validados para faturamento. |
| Glosa | Valor não faturável decorrente de OS executada porém reprovada na fiscalização. |
| Polo / Hub | Base operacional regional (Central, Norte, Sul) com equipes e almoxarifado próprios. |
| Kit | Conjunto padronizado de materiais necessário à execução de um tipo de serviço. |
| RPA | Arquivo gerado para consumo por automação de processos junto ao sistema da concessionária. |
| PP | Indicador de pré-programação/prioridade da OS na fila de tratamento. |
| Trava de histórico | Regra que limita a saída de kits ao volume executado no dia anterior. |

# **2\. Visão geral do sistema**

## **2.1 Agrupamento funcional em macro-processos**

Os nove módulos do GeniOS foram agrupados em cinco macro-processos, refletindo a sequência natural do fluxo operacional e as fronteiras de responsabilidade entre as áreas. Este agrupamento organiza a especificação e orienta o faseamento da entrega.

| Macro-processo | Módulos | Responsável típico |
| :---- | :---- | :---- |
| A. Ingestão e Preparação de Dados | Importação; Webscraper; Gerenciar Pendências | Analista de Operações |
| B. Planejamento e Despacho | Despacho & Rotas / Roteirizador; Configurações (Equipes) | Coordenador de Campo |
| C. Suprimentos e Logística | Almoxarifado | Almoxarife / Polo |
| D. Fechamento, Auditoria e Faturamento | Auditoria & Fechamento; Gerencial | Gerente de Contrato |
| E. Inteligência e Suporte à Decisão | Assistente GeniOS | Transversal (todos os perfis) |

## **2.2 Atores e perfis de acesso**

| Perfil | Atribuições no sistema |
| :---- | :---- |
| Gerente de Contrato | Visão consolidada de todos os polos; aprova forçar validação; acessa indicadores financeiros e prévia de BM. |
| Coordenador de Campo | Cria e finaliza rotas, atribui equipes, define prioridades e gera arquivo RPA. |
| Analista de Operações | Executa importações, trata pendências, desconsidera OSs e acompanha o log de divergências. |
| Almoxarife | Registra saída de kits, confirma envios e recebimentos entre polos. |
| Auditor / Faturista | Sobe a planilha de execução, edita a grade de auditoria e trata invalidações. |
| Administrador | Cadastra equipes, usuários, perfis e parâmetros do sistema (kits, prazos, tabela de preços). |

## **2.3 Contexto multi-polo**

Toda a operação do GeniOS ocorre sob um seletor global de polo, disponível de forma persistente no cabeçalho da aplicação, com as opções: Todos, Polo 1 – Central, Polo 2 – Norte e Polo 3 – Sul. A seleção condiciona simultaneamente as listagens, os filtros, os mapas, os saldos de almoxarifado e os indicadores gerenciais.

| Opção | Comportamento esperado |
| :---- | :---- |
| Todos | Agrega os dados dos três polos; indicadores somados e listagens com coluna de polo visível. Ações de escrita que dependem de um polo específico (saída de kit, criação de rota) ficam bloqueadas até a seleção de um polo. |
| Polo 1 – Central | Restringe dados, equipes e estoque ao polo Central. |
| Polo 2 – Norte | Restringe dados, equipes e estoque ao polo Norte. |
| Polo 3 – Sul | Restringe dados, equipes e estoque ao polo Sul. |

## **2.4 Ciclo de vida da Ordem de Serviço**

O estado da OS é o eixo que integra os macro-processos. A transição entre estados é a principal fonte de regras de negócio do sistema.

| \# | Estado | Transição / evento | Módulo |
| :---- | :---- | :---- | :---- |
| 1 | Importada | Upsert concluído a partir da planilha GSAN | Importação |
| 2 | Pendente | OS válida aguardando tratamento | Gerenciar Pendências |
| 3 | Desconsiderada | Ação manual do analista (estado terminal) | Gerenciar Pendências |
| 4 | Apta a roteirizar | Tratamento concluído e coordenadas presentes | Pendências / Webscraper |
| 5 | Roteirizada | Vinculada a uma rota com equipe e data | Roteirizador |
| 6 | Despachada | Rota finalizada e arquivo RPA gerado | Despacho & Rotas |
| 7 | Executada | Retorno da planilha de execução do GSAN | Auditoria & Fechamento |
| 8 | Invalidada | Reprovação pela fiscalização da concessionária | Auditoria & Fechamento |
| 9 | Validada | Aprovada na auditoria ou validação forçada | Auditoria & Fechamento |
| 10 | Faturada | Incluída no BM do ciclo (estado terminal) | Gerencial |

# **3\. Requisitos funcionais**

Os requisitos são identificados no formato RF-\<MÓDULO\>-\<nº\> e as regras de negócio associadas no formato RN-\<nº\>. Requisitos marcados como (Obrigatório) compõem o MVP; os demais são desejáveis para a evolução do produto.

# **Macro-processo A — Ingestão e Preparação de Dados**

Objetivo: transformar o arquivo bruto diário do GSAN em uma carteira de OSs confiável, geolocalizada e livre de registros fora de escopo, pronta para o planejamento. É o macro-processo com maior impacto na qualidade de todos os demais.

## **A.1 Módulo Importação**

**REQUISITOS**

**RF-IMP-01 —** O sistema deve permitir o upload da planilha bruta do GSAN em formato .xlsx, com limite de 25 MB, por arrastar-e-soltar ou seleção manual do arquivo. (Obrigatório)

**RF-IMP-02 —** O sistema deve validar, antes do processamento, a extensão, o tamanho e a aderência do arquivo ao layout esperado do GSAN, rejeitando-o com mensagem específica quando houver colunas obrigatórias ausentes.

**RF-IMP-03 —** O sistema deve filtrar automaticamente as OSs pertencentes às unidades do escopo contratual, descartando as demais e contabilizando-as como "fora de escopo". (Obrigatório)

**RF-IMP-04 —** O sistema deve executar upsert dos registros, inserindo OSs novas e atualizando as existentes sem descartar informações previamente tratadas (prioridade, equipe atribuída, marcação de desconsiderada). (Obrigatório)

**RF-IMP-05 —** O sistema deve exibir o progresso da importação em tempo real, informando percentual concluído, nome do arquivo, total de linhas e etapa corrente do processamento.

**REGRAS DE NEGÓCIO**

**RN-01 —** *A chave de identificação para o upsert é a combinação Número da Ordem de Serviço \+ Polo.*

**RN-02 —** *Campos tratados manualmente no GeniOS (prioridade, equipe, desconsideração) prevalecem sobre os valores reimportados do GSAN.*

**RN-03 —** *Uma OS ignorada por estar fora de escopo não é persistida na carteira, mas é contabilizada no resumo e no log.*

## **A.2 Módulo Webscraper**

**REQUISITOS**

**RF-WEB-01 —** O sistema deve capturar automaticamente as coordenadas geográficas (latitude e longitude) das unidades a partir do portal GSAN. (Obrigatório)

**RF-WEB-02 —** O sistema deve exibir indicador de progresso da captura no cabeçalho da aplicação, no formato "unidades processadas / total de unidades".

**RF-WEB-03 —** O sistema deve registrar as unidades cuja captura falhou, permitindo reprocessamento seletivo.

**RF-WEB-04 —** O sistema deve permitir o preenchimento manual de coordenadas para unidades não resolvidas automaticamente.

**RF-WEB-05 —** O sistema deve manter cache das coordenadas já obtidas, evitando nova captura para unidades inalteradas.

**REGRAS DE NEGÓCIO**

**RN-04 —** *OS sem coordenada válida não pode ser roteirizada pelo mapa, permanecendo em pendência até resolução.*

**RN-05 —** *A captura deve respeitar limites de requisição do portal de origem e as diretrizes de proteção de dados aplicáveis.*

## **A.3 Módulo Gerenciar Pendências**

**REQUISITOS**

**RF-PEN-01 —** O sistema deve listar as OSs importadas que exigem tratamento antes do despacho. (Obrigatório)

**RF-PEN-02 —** O sistema deve disponibilizar filtros rápidos por status, cada um com contador de OSs correspondente. (Obrigatório)

**RF-PEN-03 —** A listagem deve exibir, no mínimo, as colunas: Ordem de Serviço, Especificação, Tipo, Nº do Imóvel, Data de Geração, Unidade Atual, Cidade, Setor, Quadra, Longitude, Latitude, Prazo (h), Abertura, Decorrido, Atraso, Tipo/Equipe, Prioridade e PP. (Obrigatório)

**RF-PEN-04 —** O sistema deve calcular e destacar visualmente o tempo decorrido e o atraso de cada OS em relação ao prazo contratual. (Obrigatório)

**RF-PEN-05 —** O sistema deve permitir a ação "Desconsiderar", removendo a OS da fila de importação sem afetar as demais. (Obrigatório)

**REGRAS DE NEGÓCIO**

**RN-06 —** *Atraso \= (data/hora atual − data/hora de abertura) − prazo contratual em horas; valores positivos caracterizam OS em atraso.*

**RN-07 —** *OS desconsiderada não é roteirizada, não compõe a produção bruta e não integra o BM.*

**Macro-processo B — Planejamento e Despacho**

Objetivo: converter a carteira de OSs aptas em rotas executáveis, respeitando geografia, capacidade das equipes e prioridades contratuais, e entregar o despacho ao sistema da concessionária.

## **B.1 Módulo Configurações (Equipes)**

Módulo de cadastro que sustenta o Roteirizador; especificado antes por precedência funcional.

**REQUISITOS**

**RF-EQP-01 —** O sistema deve permitir cadastrar, editar e inativar equipes com os atributos: nome, cor de identificação, placa do veículo, status, líder, membros, região de atuação e capacidade diária de OSs. (Obrigatório)

**RF-EQP-02 —** O sistema deve exibir o total de equipes ativas disponíveis para roteirização no polo selecionado. (Obrigatório)

**RF-EQP-03 —** O sistema deve vincular cada equipe a um polo, impedindo sua utilização em rotas de outro polo.

**RF-EQP-04 —** O sistema deve permitir cadastrar os profissionais e ajudantes elegíveis à composição das equipes.

**RF-EQP-05 —** O sistema deve impedir a inativação de equipe com rotas em aberto, exigindo prévia realocação.

## **B.2 Módulo Despacho & Rotas / Roteirizador**

**REQUISITOS — SELEÇÃO E VISUALIZAÇÃO**

**RF-ROT-01 —** O sistema deve permitir selecionar a operação (ex.: PSS, XPT Express, Litoral) e a data da rota. (Obrigatório)

**RF-ROT-02 —** O sistema deve oferecer as visualizações Lista e Card para o conjunto de OSs em planejamento. (Obrigatório)

**REQUISITOS — MONTAGEM DA ROTA**

**RF-ROT-07 —** O sistema deve permitir seleção múltipla de OSs por desenho de polígono sobre o mapa. (Obrigatório)

**RF-ROT-08 —** O sistema deve exibir o contador de OSs selecionadas e permitir limpar a seleção corrente. (Obrigatório)

**REQUISITOS — DESPACHO**

**RF-ROT-16 —** O sistema deve permitir finalizar o planejamento do dia, consolidando as rotas criadas. (Obrigatório)

**RF-ROT-17 —** O sistema deve gerar o arquivo RPA a partir das rotas finalizadas, no layout exigido pela automação junto ao GSAN. (Obrigatório)

**REGRAS DE NEGÓCIO**

**RN-08 —** *Somente OSs no estado "Apta a roteirizar", com coordenada válida e não desconsideradas, podem ser incluídas em rota.*

**RN-09 —** *A equipe atribuída deve pertencer ao polo da OS e estar com status ativo na data da rota.*

**RN-10 —** *A geração do arquivo RPA transiciona as OSs da rota para o estado "Despachada", bloqueando novas edições de atribuição.*

# **Macro-processo C — Suprimentos e Logística**

Objetivo: garantir que as equipes recebam os materiais necessários à execução das rotas, com controle de consumo aderente à produção real e rastreabilidade das transferências entre polos.

## **C.1 Módulo Almoxarifado**

**REQUISITOS — SAÍDA DE KITS**

**RF-ALM-01 —** O sistema deve permitir registrar a saída de kits informando hub, equipe, tipo de kit e quantidade. (Obrigatório)

**RF-ALM-02 —** O sistema deve disponibilizar os tipos de kit parametrizados (ex.: Ligação Simples, Hidrômetro, Supressão, Religação), permitindo manutenção do catálogo pelo administrador. (Obrigatório)

**RF-ALM-03 —** O sistema deve bloquear a saída quando a quantidade solicitada exceder a execução registrada no dia anterior para aquele kit — trava de histórico. (Obrigatório)

**RF-ALM-04 —** Ao bloquear a saída, o sistema deve exibir mensagem explicativa contendo o kit, a quantidade solicitada e a quantidade executada no dia anterior. (Obrigatório)

**RF-ALM-05 —** O sistema deve exibir o painel de execução do dia anterior por kit, como referência para o almoxarife. (Obrigatório)

**REQUISITOS — TRANSFERÊNCIAS ENTRE POLOS**

**RF-ALM-07 —** O sistema deve listar os envios pendentes com kit, status, destino, equipe e quantidade. (Obrigatório)

**RF-ALM-08 —** O sistema deve listar os recebimentos pendentes com kit, quantidade, origem e status "em trânsito". (Obrigatório)

**RF-ALM-09 —** O sistema deve permitir confirmar o recebimento de carga, atualizando o saldo do polo destinatário. (Obrigatório)

**RF-ALM-10 —** O sistema deve permitir registrar divergência no recebimento (quantidade menor que a enviada), gerando pendência de conciliação.

**REGRAS DE NEGÓCIO**

**RN-11 —** *Trava de histórico: quantidade\_saída(kit, D) ≤ quantidade\_executada(kit, D−1) no mesmo polo.*

**RN-12 —** *A carga permanece no estado "em trânsito" e não compõe o saldo disponível do destinatário até a confirmação do recebimento.*

**RN-13 —** *Toda liberação excepcional da trava deve registrar autor, justificativa e data/hora, compondo trilha de auditoria.*

**Macro-processo D — Fechamento, Auditoria e Faturamento**  
Objetivo: confrontar a execução declarada com a fiscalização da concessionária, tratar invalidações antes do faturamento e dar visibilidade gerencial à conversão e à glosa. É o macro-processo que determina a receita do contrato.

## **D.1 Módulo Auditoria & Fechamento**

**REQUISITOS**

**RF-AUD-01 —** O sistema deve permitir o upload da planilha de execução/fechamento do GSAN, identificada por data de referência. (Obrigatório)

**RF-AUD-02 —** O sistema deve conciliar automaticamente a planilha de execução com as OSs despachadas, sinalizando registros sem correspondência. (Obrigatório)

**RF-AUD-03 —** O sistema deve apresentar a grade de auditoria com as colunas: OS, Serviço, Equipe, Foto, Status e Valor. (Obrigatório)

**RF-AUD-04 —** O sistema deve permitir a edição inline dos campos Serviço, Equipe, Foto, Status e Valor diretamente na grade, sem abertura de telas adicionais. (Obrigatório)

**RF-AUD-05 —** O sistema deve registrar, para cada edição inline, o valor anterior, o valor novo, o autor e a data/hora. (Obrigatório)

**REGRAS DE NEGÓCIO**

**RN-14 —** *OS invalidada não compõe a produção validada nem o BM enquanto não houver validação forçada por perfil autorizado.*

**RN-15 —** *Após o fechamento do ciclo, a grade de auditoria torna-se somente leitura; alterações exigem reabertura registrada.*

**RN-16 —** *O valor de cada OS decorre do tipo de serviço e da tabela de preços vigente do contrato.*

## **D.2 Módulo Gerencial**

**REQUISITOS**

**RF-GER-01 —** O sistema deve exibir a produção bruta do período: quantidade de OSs executadas e valor correspondente em reais. (Obrigatório)

**RF-GER-02 —** O sistema deve exibir a produção validada: quantidade, percentual de conversão sobre a produção bruta e valor em reais. (Obrigatório)

**RF-GER-03 —** O sistema deve calcular e exibir o impacto financeiro da glosa potencial em aberto. (Obrigatório)

**RF-GER-04 —** O sistema deve exibir a prévia do Boletim de Medição por polo, com o valor a faturar no ciclo. (Obrigatório)

**RF-GER-05 —** O sistema deve apresentar o funil de conversão diário, evidenciando as perdas entre as etapas do ciclo de vida da OS. (Obrigatório)

**REGRAS DE NEGÓCIO**

**RN-17 —** *Taxa de conversão \= produção validada ÷ produção bruta, expressa em percentual.*

**RN-18 —** *Glosa potencial \= valor da produção bruta − valor da produção validada, no período e polo filtrados.*

**RN-19 —** *A prévia de BM considera exclusivamente OSs no estado "Validada" dentro do ciclo de medição vigente.*

**Macro-processo E — Inteligência e Suporte à Decisão**

Objetivo: reduzir o tempo entre a pergunta de negócio e a ação, oferecendo consulta em linguagem natural sobre os dados operacionais e atalhos para execução de tarefas.

## **E.1 Módulo Assistente GeniOS**

**REQUISITOS**

**RF-ASS-01 —** O sistema deve disponibilizar assistente conversacional acessível de qualquer tela, com indicador de disponibilidade (online/offline). (Obrigatório)

**RF-ASS-02 —** O assistente deve interpretar perguntas em linguagem natural sobre a carteira de OSs, produção, equipes e faturamento. (Obrigatório)

**RF-ASS-03 —** O assistente deve apresentar respostas estruturadas, incluindo detalhamento de BM por item e valor total. (Obrigatório)

**RF-ASS-04 —** O assistente deve oferecer sugestões acionáveis que disparem operações no sistema, como atribuir despacho a uma equipe. (Obrigatório)

**RF-ASS-05 —** Ações disparadas pelo assistente devem exigir confirmação explícita do usuário antes da efetivação. (Obrigatório)

**REGRAS DE NEGÓCIO**

**RN-20 —** *O assistente não pode expor dados de polos ou módulos aos quais o perfil do usuário não tem acesso.*

**RN-21 —** *Ações executadas pelo assistente seguem exatamente as mesmas validações e travas dos módulos correspondentes.*

# **Macro-processo F — Requisitos transversais**

**REQUISITOS**

**RF-TRV-01 —** O sistema deve exigir autenticação individual e exibir o nome e o papel do usuário conectado. (Obrigatório)

**RF-TRV-02 —** O sistema deve implementar controle de acesso por perfil, restringindo módulos e ações críticas. (Obrigatório)

**RF-TRV-03 —** O sistema deve disponibilizar seletor global de polo com as opções Todos, Central, Norte e Sul, aplicável a todas as telas. (Obrigatório)

**RF-TRV-04 —** O sistema deve manter trilha de auditoria de todas as ações que alterem dados operacionais ou financeiros. (Obrigatório)

**RF-TRV-05 —** O sistema deve confirmar visualmente a conclusão das ações do usuário por meio de notificações não bloqueantes (toasts). (Obrigatório)

**4\. Entidades de dados principais**

| Entidade | Atributos essenciais | Origem |
| :---- | :---- | :---- |
| Ordem de Serviço | Número, especificação, tipo, nº imóvel, data de geração, unidade, cidade, setor, quadra, lat/long, prazo, abertura, prioridade, PP, status, equipe, rota, valor | GSAN \+ tratamento GeniOS |
| Unidade | Código, nome, polo, coordenadas, escopo contratual | GSAN \+ Webscraper |
| Equipe | Nome, cor, placa, líder, membros, região, capacidade/dia, status, polo | Cadastro GeniOS |
| Rota | Nome, cor, data, previsão de início, carregamento, equipe/veículo, profissional, ajudante, observação, OSs vinculadas | Cadastro GeniOS |
| Kit | Tipo, descrição, materiais, polo, saldo | Cadastro GeniOS |
| Movimentação de Kit | Tipo (saída/envio/recebimento), kit, quantidade, equipe, origem, destino, status, data | Almoxarifado |
| Importação | Arquivo, data de referência, totais, divergências, usuário, data/hora | Importação |
| Invalidação | OS, motivo, inspetor, data, status de tratamento, justificativa de validação forçada | Auditoria |
| Boletim de Medição | Ciclo, polo, OSs validadas, valores por item, total | Fechamento |

# 

# 

# 

# 

# **5\. Integrações externas**

| Integração | Direção | Natureza | Frequência |
| :---- | :---- | :---- | :---- |
| GSAN — planilha de OS | Entrada | Arquivo .xlsx (upload manual ou automatizado) | Diária |
| GSAN — portal de unidades | Entrada | Captura automatizada de coordenadas (webscraper) | Sob demanda / incremental |
| GSAN — planilha de execução | Entrada | Arquivo .xlsx de fechamento | Diária / por ciclo |
| Automação RPA | Saída | Arquivo de despacho no layout da automação | Diária |
| Serviço de mapas | Entrada | Camada cartográfica e geocodificação | Contínua |

# **6\. Requisitos não funcionais**

Os requisitos não funcionais estão organizados segundo as características de qualidade da ISO/IEC 25010 e identificados no formato RNF-\<nº\>.

## **6.1 Desempenho e eficiência**

**RNF-01 —** A importação de arquivo de até 25 MB e 5.000 linhas deve ser concluída em até 3 minutos, com atualização de progresso a cada 5% de avanço.

**RNF-02 —** As telas de listagem devem renderizar a primeira página de resultados em até 2 segundos para carteiras de até 50.000 OSs.

**RNF-03 —** O mapa de despacho deve renderizar e permitir seleção por polígono de até 2.000 pins simultâneos sem degradação perceptível de interação.

**RNF-04 —** A edição inline na grade de auditoria deve persistir a alteração e retornar confirmação em até 1 segundo.

**RNF-05 —** O processamento de importações e capturas do webscraper deve ocorrer de forma assíncrona, sem bloquear a navegação do usuário.

## **6.2 Confiabilidade e integridade**

**RNF-06 —** O upsert não pode resultar em perda de registros previamente importados nem sobrescrever tratamentos manuais — princípio de "sem amnésia de registros".

**RNF-07 —** Toda importação deve ser transacional: em caso de falha, nenhum registro parcial pode ser persistido.

**RNF-08 —** A trava de histórico do almoxarifado deve ser aplicada de forma determinística no servidor, não podendo ser contornada pela interface.

**RNF-09 —** O sistema deve manter disponibilidade mínima de 99% no horário operacional (05h–20h, dias úteis).

**RNF-10 —** Rotinas de backup diário com retenção mínima de 30 dias e procedimento de restauração testado.

## **6.3 Segurança e controle de acesso**

**RNF-11 —** O acesso deve ser autenticado individualmente, com política de senha forte e expiração de sessão por inatividade.

**RNF-12 —** Ações críticas — forçar validação, desconsiderar OS, liberar a trava de histórico e reabrir ciclo fechado — devem ser restritas a perfis autorizados e sempre registradas.

**RNF-13 —** As comunicações devem trafegar sobre canal criptografado (TLS) e os dados sensíveis devem ser protegidos em repouso.

**RNF-14 —** O tratamento de dados de titulares (endereços e imóveis) deve observar a LGPD, restringindo o acesso ao mínimo necessário à finalidade operacional.

## **6.4 Auditabilidade e rastreabilidade**

**RNF-15 —** Toda alteração de dado operacional ou financeiro deve registrar autor, data/hora, valor anterior e valor novo.

**RNF-16 —** A trilha de auditoria deve ser imutável e consultável por OS, usuário e período, com retenção mínima equivalente à vigência do contrato.

**RNF-17 —** Cada geração de arquivo RPA e cada fechamento de ciclo devem ser rastreáveis até o conjunto exato de OSs que os compôs.

## **6.5 Usabilidade**

**RNF-18 —** As tarefas recorrentes de auditoria devem ser executáveis por edição inline, dispensando navegação entre telas.

**RNF-19 —** O sistema deve fornecer mensagens de erro específicas e acionáveis, indicando a causa e o caminho de correção (ex.: bloqueio da trava de histórico).

**RNF-20 —** Listagens vazias devem apresentar estado informativo explicando a ausência de dados e o próximo passo esperado.

**RNF-21 —** A interface deve ser integralmente em português do Brasil, com formatação nacional de datas, números e moeda.

**RNF-22 —** O sistema deve manter consistência visual e de comportamento entre os módulos (padrões de filtro, tabela, seleção múltipla e confirmação).

## **6.6 Compatibilidade e portabilidade**

**RNF-23 —** A aplicação deve funcionar nas versões correntes dos navegadores Chrome, Edge e Firefox.

**RNF-24 —** As telas devem manter usabilidade em resoluções a partir de 1366×768 e permanecer utilizáveis em tablets para uso em campo.

**RNF-25 —** Importações e exportações devem utilizar formatos abertos e amplamente suportados (.xlsx, .csv, .pdf).

## **6.7 Escalabilidade e manutenibilidade**

**RNF-26 —** A arquitetura deve suportar a inclusão de novos polos e novas operações sem alteração estrutural do modelo de dados.

**RNF-27 —** Catálogos de kits, tipos de serviço, prazos contratuais e tabela de preços devem ser parametrizáveis pelo administrador, sem necessidade de nova versão do software.

**RNF-28 —** O sistema deve registrar logs técnicos de aplicação e de integração, com nível configurável, para diagnóstico de falhas.

# **7\. Premissas, restrições e dependências**

**PR-01 —** O layout da planilha do GSAN permanece estável; alterações de layout exigem manutenção no parser de importação.

**PR-02 —** A execução em campo é registrada no GSAN pelas equipes; o GeniOS consome o resultado, não o produz.

**PR-03 —** O acesso ao portal do GSAN pelo webscraper depende de credenciais válidas e de estabilidade do portal de origem.

**PR-04 —** A tabela de preços e os prazos contratuais são fornecidos pela gestão do contrato e mantidos como parâmetro do sistema.

**PR-05 —** O aplicativo de campo e a emissão fiscal não fazem parte desta versão e podem exigir integração futura.

# **8\. Sugestão de faseamento**

| Fase | Escopo | Justificativa |
| :---- | :---- | :---- |
| Fase 1 — Fundação | Macro-processo A (Importação, Webscraper, Pendências) \+ transversais | Sem dados confiáveis e geolocalizados nenhum outro módulo entrega valor. |
| Fase 2 — Operação | Macro-processo B (Equipes, Roteirizador, RPA) | Habilita o ganho operacional imediato: despacho estruturado. |
| Fase 3 — Receita | Macro-processo D (Auditoria & Fechamento, Gerencial) | Endereça a glosa, de maior impacto financeiro direto. |
| Fase 4 — Controle e inteligência | Macro-processo C (Almoxarifado) \+ E (Assistente) | Otimizações sobre uma base já estabilizada. |

