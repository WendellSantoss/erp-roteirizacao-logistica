---
id: HU-F13
titulo: Monitorar a disponibilidade e garantir backup restaurável
ordem: 13
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-09, RNF-10, RNF-28]
depende_de: [HU-F10]
---

# HU-F13 — Monitorar a disponibilidade e garantir backup restaurável

## História
Como **grupo do GeniOS**, queremos **saber quando o sistema cai e ter backup diário que de fato
restaura**, para **cumprir 99% de disponibilidade no horário operacional (RNF-09) e não perder
dados de faturamento (RNF-10)**.

## Regras
- **RNF-09** — 99% de disponibilidade das 05h às 20h em dias úteis (≈ 3 h fora do ar por mês, no máximo).
- **RNF-10** — Backup diário, retenção de 30 dias, restauração testada.

## Critérios de aceite
CA01 — Monitor
Dado o ambiente publicado
Quando `/api/health` fica sem responder por 2 min no horário operacional
Então o grupo recebe alerta (e-mail ou canal do grupo).

CA02 — Medição
Dado o fim do mês
Quando consulto o monitor
Então vejo o percentual de disponibilidade no horário operacional.

CA03 — Backup
Dado o banco de produção
Quando passa um dia
Então existe um backup novo, e backups com mais de 30 dias são apagados.

CA04 — Restauração testada
Dado o backup mais recente
Quando executo o procedimento documentado em `docs/operacao/restauracao.md` num banco vazio
Então o sistema sobe com os dados do backup (teste mensal registrado).
