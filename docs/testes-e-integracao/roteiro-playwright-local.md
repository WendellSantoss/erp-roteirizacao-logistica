# Roteiro Playwright Local — Evidência de Testes Ponta a Ponta

**Projeto:** GeniOS — ERP Operacional para Roteirização, Controle Logístico e Auditoria de Contratos  
**Repositório:** [WendellSantoss/erp-roteirizacao-logistica](https://github.com/WendellSantoss/erp-roteirizacao-logistica)  
**Etapa:** 7 — Integração e testes  
**Data da execução:** 21/11/2026 (registrada em `docs/registro-uso-ia.md`)  
**Ambiente:** execução local (navegador controlado via Playwright) + verificação complementar nas URLs publicadas

> **Natureza deste documento**  
> Este arquivo formaliza o roteiro de testes ponta a ponta executados localmente com Playwright durante a Etapa 6/7.  
> Não existe suíte automatizada de e2e versionada no repositório (apenas testes unitários com Vitest).  
> O resultado **aprovado** foi relatado pela equipe no registro de uso de IA e é corroborado pelas **104 capturas de tela** já anexadas em `docs/testes-e-integracao/evidencias/`.

---

## 1. Objetivo

Validar, de ponta a ponta, os fluxos das **cinco histórias prioritárias** do MVP:

1. Acesso e filtro global por polo (HU-019 e HU-020)
2. Upload, validação de layout e filtro de escopo GSAN (HU-001, HU-002 e HU-003)
3. Importação transacional com upsert sem amnésia (HU-004)
4. Listagem e tratamento de pendências de OS (HU-006, HU-007 e HU-008)
5. Bloqueio de saída de kit por trava de histórico (HU-016)

Além dos fluxos funcionais, o roteiro incluiu verificação de responsividade em **390 px** de largura (sem rolagem horizontal indesejada).

---

## 2. Ambiente e pré-condições

| Item | Valor |
|------|--------|
| Frontend | Aplicação local (Vite) apontando para a API no Render / Neon |
| Backend | API publicada no Render (`https://genios-api-kruh.onrender.com`) |
| Banco | PostgreSQL no Neon com dados de demonstração (`popular_dados_demo`) |
| Usuários de teste | Seeds: Ana (Analista), Bruno (Analista Polo 2), Carlos (Almoxarife), Gabriela (Gerente), Alice (Auditora), Davi (Admin) |
| Ferramenta | Playwright (execução local controlada) |
| Resolução adicional | 390 px de largura (mobile) |

---

## 3. Roteiro executado

### 3.1 História 1 — Acesso e filtro global por polo (HU-019 / HU-020)

**Passos:**
1. Acessar a tela de login
2. Tentar login com credenciais inválidas → mensagem de erro
3. Realizar 5 tentativas inválidas → bloqueio temporário
4. Login bem-sucedido com usuário Analista (Ana)
5. Verificar exibição de nome e perfil
6. Selecionar um polo específico
7. Tentar acessar dados de outro polo → restrição aplicada
8. Selecionar “Todos os polos” → ações de escrita bloqueadas
9. Verificar restrições de menu por perfil (Analista sem acesso ao Almoxarifado)

**Resultado:** Aprovado  
**Evidências visuais:**  
`evidencias/0-geral/01-login.png`  
`evidencias/0-geral/02-login-credenciais-invalidas.png`  
`evidencias/0-geral/03-login-bloqueado-5-tentativas.png`  
`evidencias/1-ana-analista/07-almoxarifado-sem-acesso.png`  
`evidencias/2-bruno-analista-polo2/02-pendencias.png`

---

### 3.2 História 2 — Upload, validação e filtro de escopo (HU-001 / HU-002 / HU-003)

**Passos:**
1. Login como Analista
2. Enviar planilha `.xlsx` válida → resumo e hash apresentados
3. Enviar arquivo com formato inválido → rejeição clara
4. Enviar planilha sem colunas obrigatórias → erro 422 com lista de colunas faltantes
5. Verificar filtragem de OSs fora do escopo do polo
6. Conferir alertas de importação

**Resultado:** Aprovado  
**Evidências visuais:**  
`evidencias/1-ana-analista/20-importacao-resultado-com-alertas.png`  
`evidencias/1-ana-analista/23-importacao-fora-de-escopo.png`  
`evidencias/1-ana-analista/24-importacao-colunas-ausentes.png`  
`evidencias/1-ana-analista/25-importacao-formato-invalido.png`

---

### 3.3 História 3 — Importação transacional com upsert (HU-004)

**Passos:**
1. Importar OSs novas
2. Reimportar o mesmo arquivo → ausência de duplicatas
3. Verificar preservação de prioridade e equipe atribuídas manualmente
4. Verificar preservação de estados terminais
5. Confirmar comportamento de rollback em falha (cenário de teste)

**Resultado:** Aprovado  
**Evidências visuais:**  
`evidencias/1-ana-analista/21-importacao-mesmo-arquivo-novamente.png`  
`evidencias/1-ana-analista/22-importacao-atualizacao-upsert.png`  
`evidencias/1-ana-analista/20-importacao-resultado-com-alertas.png`

---

### 3.4 História 4 — Listagem e tratamento de pendências (HU-006 / HU-007 / HU-008)

**Passos:**
1. Listar OSs do polo selecionado
2. Aplicar filtro de atraso
3. Marcar OS como prioritária
4. Desconsiderar OS com justificativa
5. Verificar registro correspondente na trilha de auditoria

**Resultado:** Aprovado  
**Evidências visuais:**  
`evidencias/1-ana-analista/02-pendencias-todos-os-polos.png`  
`evidencias/1-ana-analista/11-pendencias-so-em-atraso.png`  
`evidencias/1-ana-analista/15-pendencias-os-priorizada.png`  
`evidencias/1-ana-analista/19-pendencias-os-desconsiderada.png`  
`evidencias/4-gabriela-gerente/09-auditoria-todos-os-polos.png`

---

### 3.5 História 5 — Bloqueio de saída de kit (HU-016)

**Passos:**
1. Login como Almoxarife (Carlos)
2. Consultar limites de kits por equipe (baseado em D-1)
3. Registrar saída dentro do limite → sucesso
4. Tentar registrar saída que excede o executado em D-1 → bloqueio com mensagem clara
5. Verificar que a saída excedente **não** foi registrada
6. Confirmar registro da tentativa na auditoria

**Resultado:** Aprovado  
**Evidências visuais:**  
`evidencias/3-carlos-almoxarife/04-almoxarifado.png`  
`evidencias/3-carlos-almoxarife/07-almoxarifado-saida-registrada.png`  
`evidencias/3-carlos-almoxarife/08-almoxarifado-saida-bloqueada.png`  
`evidencias/3-carlos-almoxarife/09-almoxarifado-apos-bloqueio.png`

---

### 3.6 Responsividade

O mesmo roteiro foi reexecutado em viewport de **390 px** de largura.  
**Resultado:** nenhuma rolagem horizontal indesejada; fluxos principais operáveis.

---

## 4. Resultado consolidado

| História prioritária | Resultado do roteiro | Evidência visual principal |
|----------------------|----------------------|----------------------------|
| 1. Acesso e filtro por polo | Aprovado | Login + restrições de perfil/polo |
| 2. Upload e validação de planilha | Aprovado | Resultado de importação + erros de layout |
| 3. Upsert transacional | Aprovado | Reimportação do mesmo arquivo |
| 4. Pendências | Aprovado | Lista, prioridade, desconsideração e auditoria |
| 5. Trava de kits | Aprovado | Saída bloqueada + estado após bloqueio |
| Responsividade (390 px) | Aprovado | Fluxos principais operáveis |

**Status geral do roteiro Playwright local:** **Aprovado**

---

## 5. Limitações e transparência

- Não há suíte Playwright versionada no repositório (apenas testes unitários com Vitest).
- O log bruto do terminal da execução local não foi preservado no momento da execução.
- Este documento reconstrói formalmente o roteiro e o resultado com base no registro da equipe (`docs/registro-uso-ia.md`) e no acervo de 104 capturas já existentes.
- Critérios que dependem de comportamento interno (atomicidade, ausência de duplicatas, preservação de campos) continuam lastreados prioritariamente pelos **101 testes automatizados de backend** e pelo smoke test publicado.

---

## 6. Referências

- Relatório principal da Etapa 7: [`relatorio-testes-etapa-7.md`](./relatorio-testes-etapa-7.md)
- Registro de uso de IA: [`../registro-uso-ia.md`](../registro-uso-ia.md)
- Índice de evidências visuais: [`evidencias/README.md`](./evidencias/README.md)
- Histórias prioritárias: [`../historias-priorizadas.md`](../historias-priorizadas.md)
