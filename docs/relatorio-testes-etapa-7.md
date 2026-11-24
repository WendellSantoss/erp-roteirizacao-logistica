# Etapa 7 — Integração e testes

**Projeto:** GeniOS — ERP Roteirização Logística  
**Data do relatório:** 24/11/2026  
**Branch:** `docs/etapa-7-integracao-testes`  
**Commit-base avaliado:** `38f08bcdf1aec322a8c84b04c5d274039878e8e0` (`main`, 23/11/2026)

## 1. Objetivo

Validar os critérios de aceite do MVP ponta a ponta, verificar os testes automatizados existentes e registrar a situação da versão publicada. Este relatório diferencia testes automatizados aprovados de verificações de integração em produção que não puderam ser concluídas.

## 2. Evidências de testes automatizados

Foi consultada a execução do GitHub Actions **Qualidade**, execução #14, disparada em 23/11/2026 para o commit-base indicado acima:

[Execução #14 — GitHub Actions](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45166789298)

| Verificação | Resultado registrado | Evidência |
|---|---:|---|
| Backend — testes com PostgreSQL 17 | **Aprovado: 101 testes** | Log: `Ran 101 tests in 17.870s — OK` |
| Frontend — Vitest | **Aprovado: 9 testes** | 2 arquivos aprovados; 9 testes aprovados |
| Frontend — formatação Prettier | **Aprovado** | `All matched files use Prettier code style!` |
| Frontend — ESLint | **Aprovado** | Etapa concluída com sucesso |
| Frontend — build de produção | **Aprovado** | TypeScript e Vite concluídos; `built` |
| Backend — Ruff format | **Aprovado** | Etapa concluída com sucesso |
| Backend — Ruff lint | **Aprovado** | Etapa concluída com sucesso |
| Backend — regras de dependência entre módulos | **Aprovado** | 3 contratos mantidos; 0 quebrados |
| Backend — sincronização das migrations | **Aprovado** | `makemigrations --check --dry-run` concluído |

**Resultado da CI:** os jobs `backend` e `frontend` da execução #14 terminaram com conclusão `success`.

## 3. Critérios de aceite cobertos pelos testes existentes

Conforme o mapa de testes documentado em `docs/processo/etapas-5-e-6.md`, a suíte de backend cobre:

- **HU-019 — Login:** autenticação, bloqueio e ciclo do token.
- **HU-020 — Perfil e polo:** matriz de permissões, restrições de leitura/escrita e respostas `403`/validações.
- **HU-F11 — Ciclo de vida da OS:** transições permitidas e rejeição das demais.
- **HU-001 a HU-004 — Importação:** validação de arquivo/layout, escopo por polo, upsert e integridade transacional.
- **HU-006 a HU-008 — Pendências:** consulta, prioridade, desconsideração e auditoria.
- **HU-016 — Trava de kit:** limites, bloqueios e concorrência.

A suíte de frontend registra testes para os utilitários de planilha e formatação (9 testes no total). A verificação automatizada de `/health` também possui testes no backend: resposta de sucesso com API e banco OK, e resposta de indisponibilidade do banco sem exposição de detalhes internos.

## 4. Verificação da integração publicada

O README identifica os seguintes ambientes:

- Frontend: https://erp-roteirizacao-logistica-so5e.vercel.app
- Health check da API: https://genios-api-kruh.onrender.com/health

**Situação: pendente de confirmação externa nesta execução.** A tentativa de acessar as URLs publicadas a partir do ambiente de execução não conseguiu resolver os domínios (falha de DNS/rede). Portanto, não foi possível registrar um status HTTP real, confirmar a mensagem `API OK · Banco OK` no frontend, nem concluir um fluxo de navegador autenticado entre Vercel → Render → Neon. Não se deve interpretar a ausência dessa evidência como aprovação ou como falha definitiva dos serviços.

O teste automatizado de `/health` no backend não substitui a verificação do serviço publicado.

## 5. Observações encontradas nos logs

- A instalação do frontend registrou **7 vulnerabilidades moderadas** no relatório do npm. A pipeline não falhou por esse aviso; recomenda-se avaliar `npm audit` separadamente antes de atualizar dependências.
- Foram exibidos avisos de depreciação do módulo `punycode` e das versões Node 20 utilizadas indiretamente por actions. Não impediram a execução.
- O log PostgreSQL contém erros esperados por testes negativos, incluindo violações de unicidade, constraints e tentativas de alteração/exclusão de registros de auditoria imutáveis. A suíte terminou com `OK`.

## 6. Conclusão e situação da versão

**Aprovado:** a integração contínua do commit-base executou com sucesso os testes automatizados de backend e frontend, as verificações estáticas, a validação das migrations e a compilação de produção do frontend.

**Pendente para declarar a validação ponta a ponta integralmente concluída:** executar e registrar, em ambiente com acesso às URLs publicadas, o fluxo real frontend → API → PostgreSQL, incluindo a tela de saúde e os fluxos autenticados previstos nos critérios de aceite. Também é necessário anexar evidência verificável dessa sessão (por exemplo, capturas de tela e horário da execução).

Esta branch contém o relatório da Etapa 7. A branch `main` não foi alterada. Não foi realizada publicação de nova versão em Vercel/Render nem merge automático. A versão final só deve ser considerada integralmente validada após a conclusão da verificação externa pendente.

## 7. Referências do projeto

- [Repositório GeniOS](https://github.com/WendellSantoss/erp-roteirizacao-logistica)
- [Workflow de qualidade — execução #14](https://github.com/WendellSantoss/erp-roteirizacao-logistica/actions/runs/45166789298)
- `docs/processo/etapas-5-e-6.md` — mapa história → endpoints → tela → testes
- `backend/nucleo/tests/test_health.py` — testes do health check
- `frontend/package.json` — comandos de teste, lint, formatação e build
