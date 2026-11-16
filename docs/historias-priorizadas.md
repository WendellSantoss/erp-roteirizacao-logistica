# Histórias de Usuário Priorizadas — Escopo do Protótipo (MVP)

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