---
id: HU-F04
titulo: Criar o esqueleto do frontend
ordem: 4
modulo: Fundação
epico: EP-0 Fundação técnica
tela: —
fase: 0
prioridade: MVP
status: rascunho
requisitos: []
regras: []
nao_funcionais: [RNF-21, RNF-22, RNF-24]
depende_de: [HU-F02]
---

# HU-F04 — Criar o esqueleto do frontend

## História
Como **desenvolvedor do GeniOS**, quero **um projeto React com o layout do protótipo, o design
system e os componentes base prontos**, para **que as telas de cada módulo sejam montadas com
peças iguais (RNF-22) em vez de cada tela inventar a sua tabela, filtro e botão**.

## Contexto
O protótipo (`GeniOS ERP.html`) usa o design system "Industry": tokens em CSS (`--color-*`,
`--font-*`, `--space-*`), Barlow / Barlow Condensed, ícones Lucide com traço 1.5. O layout tem
menu lateral com os módulos, cabeçalho com seletor de polo, indicador do webscraper e usuário.

## Critérios de aceite
CA01 — Layout base
Dado o frontend em execução
Quando abro a aplicação
Então vejo o menu lateral com os módulos do protótipo, o cabeçalho com o espaço do seletor de
polo e do usuário, e cada item de menu abre uma página vazia com título.

CA02 — Tokens do design system
Dado o código do frontend
Quando procuro cores ou fontes escritas direto (`#5980a6`, `Barlow`) fora do arquivo de tokens
Então não encontro nenhuma; tudo usa as variáveis do design system.

CA03 — Componentes base
Dado a pasta de componentes compartilhados
Quando listo
Então existem Tabela, Filtro rápido com contador, Botão, Campo, Diálogo de confirmação, Toast e
Estado vazio, cada um com um teste.

CA04 — Formato brasileiro (RNF-21)
Dado os utilitários de formatação
Quando formato `1234.5` como moeda e `2026-07-11T08:12` como data
Então obtenho `R$ 1.234,50` e `11/07/2026 08:12`.

CA05 — Resolução mínima (RNF-24)
Dado a janela em 1366×768
Quando navego por todas as páginas
Então não há rolagem horizontal na página (tabelas largas rolam dentro do próprio contêiner).

CA06 — Testes e lint
Dado o frontend
Quando executo `npm run lint`, `npm run typecheck` e `npm test`
Então os três terminam sem erro.

## Fora de escopo
Telas de negócio; seletor de polo funcional (HU-054); login (HU-019).
