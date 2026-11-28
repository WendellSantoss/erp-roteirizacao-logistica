# Histórias de Usuário Priorizadas — Escopo do Protótipo (MVP + Incremento 2)

Em alinhamento com a **Fase 1 (Fundação)** da Especificação de Requisitos (ERS) e com os atributos de qualidade prioritários do **ADR-001** (integridade dos dados, segurança das regras e auditabilidade), foram selecionadas **5 histórias de usuário prioritárias ("must have")** para o protótipo funcional do **GeniOS**.

---

## 1. Autenticação Individual e Controle de Acesso por Perfil e Polo (`HU-019` e `HU-020`)
* **Arquivos de referência completos:** `docs/historias/HU-019-autenticacao-individual.md` e `docs/historias/HU-020-controlar-acesso-por-perfil.md`
* **Requisitos relacionados:** `RF-TRV-01`, `RF-TRV-02`, `RF-TRV-03`, `RNF-11`, `RNF-12`
* **Descrição:** Como usuário do GeniOS, quero me autenticar individualmente e filtrar toda a operação por um seletor global de polo (*Todos, Polo 1 - Central, Polo 2 - Norte, Polo 3 - Sul*), para garantir que cada perfil acesse apenas os dados e ações permitidos ao seu polo.
* **Critérios de Aceite principais:**
  * Exigir login individual com exibição do nome e perfil do usuário conectado.
  * Disponibilizar seletor global de polo persistente no cabeçalho (`Todos`, `Central`, `Norte`, `Sul`).
  * Bloquear ações de escrita (como importação e saída de kits) quando a opção `Todos` estiver selecionada, exigindo um polo específico.
  * Garantir no servidor que um usuário não visualize nem altere registros de polos não autorizados.

---

## 2. Upload, Validação de Layout e Filtro de Escopo da Planilha GSAN (`HU-001`, `HU-002` e `HU-003`)
* **Arquivos de referência completos:** `docs/historias/HU-001-upload-planilha-gsan.md`, `docs/historias/HU-002-validar-layout-da-planilha.md` e `docs/historias/HU-003-filtrar-oss-fora-de-escopo.md`
* **Requisitos relacionados:** `RF-IMP-01`, `RF-IMP-02`, `RF-IMP-03`, `RN-03`, `PR-01`
* **Descrição:** Como Analista de Operações, quero fazer o upload da planilha diária `.xlsx` do GSAN, validando seu layout e filtrando automaticamente apenas as unidades do escopo contratual, para evitar que arquivos incorretos ou OSs fora de contrato contaminem a carteira.
* **Critérios de Aceite principais:**
  * Aceitar apenas arquivos `.xlsx` com limite de até 25 MB.
  * Validar o cabeçalho antes de gravar qualquer dado; se faltar coluna obrigatória, recusar o arquivo inteiro com mensagem específica.
  * Descartar OSs de unidades fora do escopo contratual sem gravá-las na carteira, mas contabilizando o total como "fora de escopo" no resumo da importação.
  * Armazenar o hash SHA-256 do arquivo enviado para rastreabilidade.

---

## 3. Importação Transacional com Upsert Sem Amnésia (`HU-004`)
* **Arquivo de referência completo:** `docs/historias/HU-004-atualizar-oss-sem-perder-tratamento.md`
* **Requisitos relacionados:** `RF-IMP-04`, `RF-IMP-05`, `RN-01`, `RN-02`, `RNF-06`, `RNF-07`
* **Descrição:** Como Analista de Operações, quero que a importação insira novas OSs e atualize os dados vindos do GSAN nas OSs já existentes sem apagar tratamentos manuais feitos no GeniOS, para manter a integridade da carteira nas reimportações diárias.
* **Critérios de Aceite (Tabela 5 do Projeto Arquitetural):**
  * **CA01 (Novas e atualizadas):** Retornar resumo com total de OSs novas, atualizadas e fora de escopo.
  * **CA02 (Tratamento preservado):** Atualizar apenas os campos originados do GSAN (`CAMPOS_GSAN`), preservando prioridade e equipe atribuída manualmente.
  * **CA03 (Desconsiderada preservada):** OS marcada como `Desconsiderada` permanece nesse estado após nova importação.
  * **CA04 (Estado não retrocede):** A reimportação nunca retrocede o ciclo de vida de uma OS já avançada.
  * **CA05 (Sem amnésia):** OSs ausentes na nova planilha não são excluídas do banco.
  * **CA06 (Tudo ou nada):** Toda a gravação ocorre dentro de uma única transação (`transaction.atomic()`); em caso de falha, nenhum registro parcial é salvo.
  * **CA07 (Chave natural):** A unicidade da OS é garantida pela combinação `(numero, polo)`.
  * **CA08 (Desempenho):** Processar até 5.000 linhas em até 3 minutos.
  * **CA09 (Idempotência):** Reimportar o mesmo arquivo não cria duplicatas nem perde tratamentos.

---

## 4. Listagem e Tratamento de Pendências de OS (`HU-006`, `HU-007` e `HU-008`)
* **Arquivos de referência completos:** `docs/historias/HU-006-listar-oss-pendentes.md`, `docs/historias/HU-007-exibir-colunas-das-oss.md` e `docs/historias/HU-008-calcular-e-destacar-atraso.md`
* **Requisitos relacionados:** `RF-PEN-01`, `RF-PEN-02`, `RF-PEN-03`, `RF-PEN-04`, `RF-PEN-05`, `RN-06`, `RN-07`
* **Descrição:** Como Analista de Operações, quero visualizar as OSs importadas com cálculo de tempo decorrido e atraso, podendo definir prioridade ou desconsiderar OSs inválidas, para preparar a carteira antes da roteirização.
* **Critérios de Aceite principais:**
  * Listar OSs filtradas pelo polo selecionado no cabeçalho, com contadores por status.
  * Calcular atraso conforme `RN-06`: `(data/hora atual - data/hora de abertura) - prazo contratual em horas`.
  * Permitir marcar prioridade ou executar a ação "Desconsiderar" (transicionando para estado terminal `DESCONSIDERADA` e registrando na trilha de auditoria).

---

## 5. Bloqueio de Saída de Kit por Trava de Histórico (`HU-016`)
* **Arquivo de referência completo:** `docs/historias/HU-016-trava-de-historico.md`
* **Requisitos relacionados:** `RF-ALM-01`, `RF-ALM-03`, `RF-ALM-04`, `RN-11`, `RNF-08`
* **Descrição:** Como Almoxarife, quero registrar a saída de kits para as equipes com validação automática da trava de histórico no servidor, para impedir retiradas acima do volume executado no dia anterior.
* **Critérios de Aceite principais:**
  * Bloquear no servidor qualquer saída em que `quantidade_saida(kit, D) > quantidade_executada(kit, D-1)` no mesmo polo.
  * Retornar mensagem explicativa informando o tipo de kit, a quantidade solicitada e o limite executado no dia anterior.

---

# Incremento 2 — Mapa e roteirização (após a publicação do MVP)

> **Por que ampliar o escopo.** Com o MVP em produção, o sistema tratava as OSs mas parava antes do
> **mapa**, que é o centro do produto (ERS §1: "roteirização"). O grupo priorizou as histórias do
> **EP-B Planejamento e despacho** necessárias para o ciclo `Pendente → Apta → Roteirizada →
> Despachada` rodar de ponta a ponta. Decisões técnicas em `docs/adr/ADR-002-mapa-e-roteirizacao.md`.

## 6. Coordenada manual da unidade e liberação para roteirização (`HU-024` e `HU-060`)
* **Arquivos de referência:** `docs/historias/HU-024-preencher-coordenadas-manualmente.md` e `docs/historias/HU-060-concluir-tratamento-da-pendencia.md`
* **Requisitos relacionados:** `RF-WEB-04`, `RF-PEN-06` (proposto), `RN-04`, `RNF-15`
* **Descrição:** Como Analista de Operações, quero informar a coordenada das unidades que a captura não resolveu e liberar em lote as OSs tratadas, para que elas apareçam no mapa do Coordenador de Campo.
* **Critérios de Aceite principais:**
  * Coordenada digitada com vírgula ou ponto, ou marcada com clique no mapa; fora da Paraíba é recusada com "Coordenada fora da área de operação (Paraíba)".
  * Coordenada manual não é sobrescrita por captura automática; a trilha guarda valor anterior e novo.
  * Liberação em lote: OSs sem coordenada são puladas e informadas pelo número; cada transição vai para a trilha.
* **Substitui, no protótipo:** a captura automática pelo portal GSAN (`HU-005`), bloqueada por falta de acesso ao portal.

## 7. Mapa, seleção por polígono e criação de rota (`HU-011`, `HU-012`, `HU-031` e `HU-056`)
* **Arquivos de referência:** `HU-011-selecionar-operacao-e-data.md`, `HU-012-selecionar-oss-por-poligono.md`, `HU-031-contador-e-limpar-selecao.md`, `HU-056-criar-rota.md`
* **Requisitos relacionados:** `RF-ROT-01`, `RF-ROT-07`, `RF-ROT-08`, `RF-ROT-03` (proposto), `RN-08`, `RN-09`, `RNF-03`
* **Descrição:** Como Coordenador de Campo, quero escolher operação e data, desenhar um polígono no mapa para selecionar as OSs aptas e criar uma rota com equipe e horários, para que cada equipe saia com um roteiro fechado.
* **Critérios de Aceite principais:**
  * Data padrão amanhã; data passada abre só para consulta; a escolha é lembrada na sessão.
  * Só OSs aptas, com coordenada, aparecem no mapa; borda do polígono conta como dentro; novo polígono soma à seleção.
  * Contador "N OSs selecionadas", "Limpar" e aviso de capacidade máxima das equipes.
  * A rota exige nome, equipe ativa do polo, início e carregamento; bloqueia capacidade do dia excedida, OS já em outra rota e data passada; registra a criação na trilha.

## 8. Finalização do planejamento e arquivo RPA (`HU-013` e `HU-014`)
* **Arquivos de referência:** `HU-013-finalizar-planejamento.md`, `HU-014-gerar-arquivo-rpa.md`
* **Requisitos relacionados:** `RF-ROT-16`, `RF-ROT-17`, `RN-10`, `RNF-17`
* **Descrição:** Como Coordenador de Campo, quero finalizar o planejamento depois de conferir as rotas e gerar o arquivo de despacho, para que o despacho chegue à concessionária sem digitação.
* **Critérios de Aceite principais:**
  * Finalizar recusa com a lista de inconsistências (rota sem OS, equipe inativa, capacidade, OS fora de "Roteirizada"); finalizado não aceita novas rotas.
  * O RPA só é gerado com o planejamento finalizado, leva as OSs a "Despachada" (tudo ou nada) e guarda hash SHA-256; baixar de novo devolve o mesmo arquivo.
  * **Layout do arquivo é proposta do grupo** (CSV `;`), até a automação definir o oficial.

## Fora do Incremento 2 (continuam no backlog)
`HU-005/022/023/046` (webscraper), `HU-009/028` como telas de cadastro (placa e capacidade entram só
como campos da equipe, pelo seed/admin), `HU-057` (atribuir sem rota), `HU-058` (prioridade no mapa),
`HU-059` (trocar equipe ou retirar OS da rota), `HU-030` (lista × cartões) e `HU-066` como tela (as
operações vêm de migration).
