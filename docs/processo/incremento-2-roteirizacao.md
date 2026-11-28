# Incremento 2 — Mapa e roteirização (Etapas 4, 5 e 6 repetidas para o novo escopo)

* **Data:** 28/11/2026 · **Branch:** `incremento-2-roteirizacao`
* **Ferramenta de IA:** Claude Code (Claude Opus, plano Pro pago), agente no repositório com o
  `AGENTS.md` lido automaticamente
* **Escopo:** HU-024, HU-060, HU-011, HU-012, HU-031, HU-056, HU-013 e HU-014
  (`docs/historias-priorizadas.md`, seções 6 a 8; decisões em `docs/adr/ADR-002-mapa-e-roteirizacao.md`)

## 1. Por que este incremento

O MVP publicado tratava as OSs (importação, pendências) mas parava antes do mapa. As histórias acima
são o caminho mínimo para o ciclo de vida da OS (HU-F11) andar de "Pendente" até "Despachada" no
protótipo, que é o coração do produto (roteirização).

## 2. O que mudou em cada etapa anterior

| Etapa | Mudança |
|---|---|
| 1. Pacote de contexto | `historias-priorizadas.md` (seções 6–8 e o que ficou fora), `contrato-api.md` (seções 7 e 8), ADR-002, nota no README do C4, cabeçalho e "Decisões do Incremento 2" nas 8 histórias (`status: concluída`) |
| 3. Guia de código | `AGENTS.md`: módulo `roteirizacao`, arquivos `services_*.py` quando o `services.py` passaria de 300 linhas; `.importlinter` com o módulo novo nos 3 contratos |
| 4. Banco | Migrations `nucleo/0003` (coordenada manual, placa, capacidade, CHECKs) e `roteirizacao/0001–0002` (5 tabelas + operações); `modelo-dados.md` (D16–D20) e `diagrama-er.mmd`; seeds com bairros reais de João Pessoa (as coordenadas antigas eram de Fortaleza, fora da área da RN-L02), usuário Coordenador e equipes com placa/capacidade |
| 5. Backend | `nucleo/services_preparacao.py`, app `roteirizacao` (models, consultas, services, services_despacho, arquivo_rpa, views), 42 testes novos citando os CAs |
| 6. Frontend | Telas **Coordenadas** e **Roteirizador**, liberação em lote em **Pendências**; Leaflet; 8 testes Vitest novos (geometria e agrupamento) |
| 7. Integração | Fluxo percorrido no navegador local (evidências em `docs/testes-e-integracao/evidencias/incremento-2/`); CI no PR |

## 3. Revisão de código (clean code) feita junto

* A pedido do grupo, o código existente foi revisado contra o `AGENTS.md`. Ele já estava dentro dos
  limites do linter e das regras de camada; **não foi necessário reescrever** módulos do MVP. As
  correções foram pontuais:
  * seeds com coordenadas fora da área de operação e OSs "Roteirizada" sem rota (estado impossível
    depois da HU-056) — corrigidos;
  * o seed sobrescrevia coordenada e estado em toda execução — agora respeita coordenada manual e
    OSs que já estão em rota;
  * `Unidade` aceitava latitude sem longitude — CHECK no banco.
* No código novo, o ESLint barrou 4 funções acima de 60 linhas; todas foram divididas em
  componentes menores (nenhum `eslint-disable` novo, exceto o `exhaustive-deps` documentado em
  `MapaBase.tsx`).

## 4. Divergências conscientes

| Documento | Divergência | Motivo |
|---|---|---|
| C4 nível 2 (PostGIS) | Sem PostGIS | ADR-002 §2.2 |
| HU-005 | Captura automática não implementada | Sem acesso ao portal GSAN; HU-024 cobre a entrada manual |
| HU-014 CA06 | Layout RPA proposto, não oficial | Dúvida bloqueante aberta; isolado em `arquivo_rpa.py` |
| HU-031 CA01 | Sem botão "Atribuir equipe" | HU-057 fora do incremento |
| HU-056 | Sem profissional/ajudante | HU-028 fora do incremento |

## 5. Pendências de deploy

1. Merge do PR na `main` (Vercel e Render publicam a partir dela).
2. No Render, o deploy precisa rodar `python manage.py migrate` (3 migrations novas, uma delas cria
   as operações PSS, XPT Express e Litoral).
3. Rodar `popular_dados_demo` no Neon para atualizar unidades (coordenadas), equipes (placa e
   capacidade) e criar `caio.coordenador@genios.test`.
