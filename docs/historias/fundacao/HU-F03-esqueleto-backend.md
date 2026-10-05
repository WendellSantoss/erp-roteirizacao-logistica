---
id: HU-F03
titulo: Criar o esqueleto do backend
ordem: 3
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-28]
depende_de: [HU-F02]
---

# HU-F03 — Criar o esqueleto do backend

## História
Como **desenvolvedor do GeniOS**, quero **um projeto Django com API REST, testes, lint e uma
organização por módulo de negócio já definidos**, para **que cada história nova siga o mesmo
padrão em vez de cada um (ou cada agente) inventar o seu**.

## Contexto
Os módulos da ERS viram apps Django: `importacao`, `webscraper`, `pendencias`, `equipes`,
`roteirizacao`, `almoxarifado`, `auditoria`, `gerencial`, `assistente`, além de `contas`
(usuários, perfis, polos) e `nucleo` (auditoria de alterações, utilidades).

## Regras
- **RN-L01** — Regra de negócio fica em serviços (`services.py`), não em views nem serializers;
  views só traduzem HTTP. Isso permite que o assistente (RN-21) chame as mesmas regras.
- **RN-L02** — Toda consulta de dados operacionais filtra por polo do usuário (RF-TRV-03, RN-20).

## Critérios de aceite
CA01 — Saúde da API
Dado o ambiente da HU-F02 em execução
Quando chamo `GET /api/health`
Então recebo `200` com o estado do banco e do Redis.

CA02 — Estrutura por módulo
Dado o diretório `backend/`
Quando listo os apps
Então existem os apps listados no Contexto, cada um com `models.py`, `services.py`, `api/` e
`tests/`.

CA03 — Testes e lint
Dado o backend
Quando executo `pytest` e `ruff check`
Então ambos terminam sem erro, com pelo menos um teste por app.

CA04 — Logs técnicos (RNF-28)
Dado a variável `LOG_LEVEL=DEBUG`
Quando chamo qualquer endpoint
Então o log sai em JSON com nível, horário, rota e id da requisição; com `LOG_LEVEL=WARNING`, a
mesma chamada não gera log de nível INFO.

CA05 — Português do Brasil
Dado o backend
Quando uma validação falha
Então a mensagem de erro retornada está em pt-BR e o fuso padrão é `America/Fortaleza`.

## Fora de escopo
Autenticação (HU-019), perfis (HU-020), trilha de auditoria de negócio (HU-045).

## Dúvidas em aberto
- Fuso horário da operação: `America/Fortaleza` (UTC−3, sem horário de verão) assumido para a Paraíba.
