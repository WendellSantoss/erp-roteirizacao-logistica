# ADR-002 — Mapa e roteirização no Incremento 2

* **Status:** Aceita
* **Data da decisão:** 28/11/2026
* **Decisores:** equipe do projeto (proposta do Felipe de Almeida Silva, revisão do grupo no PR)
* **Decisão:** Leaflet + OpenStreetMap no frontend, seleção por polígono no navegador com
  revalidação no servidor, e layout de RPA isolado num único arquivo
* **Relação com o ADR-001:** mantém o Monólito Modular; acrescenta o módulo `roteirizacao`
  ("Planejamento e Roteirização" da lista do ADR-001)

---

## 1. Contexto

O MVP (Etapas 1–8) entregou importação, pendências, trava de kits e auditoria, mas parava antes do
mapa: as OSs eram tratadas e não havia como montá-las em rotas. O grupo decidiu ampliar o escopo
com as histórias do **EP-B Planejamento e despacho** necessárias para fechar o ciclo
`Pendente → Apta → Roteirizada → Despachada`:

| História | Por que entra |
|---|---|
| HU-024 Coordenada manual | Sem coordenada a OS não vai ao mapa (RN-04); a captura automática (HU-005) depende de acesso ao portal GSAN, que o grupo não tem |
| HU-060 Liberar para roteirização | Única forma de levar a OS de "Pendente" a "Apta" |
| HU-011 Operação e data | Toda rota pertence a polo + operação + data |
| HU-012 Polígono no mapa / HU-031 Contador | Seleção das OSs que formam a rota |
| HU-056 Criar rota | Leva as OSs a "Roteirizada" |
| HU-013 Finalizar / HU-014 Arquivo RPA | Fecha o planejamento e leva as OSs a "Despachada" |

Ficaram de fora: HU-005/022/023/046 (webscraper — sem acesso ao portal), HU-009/028 completas
(cadastro de equipes pela tela; placa e capacidade entram só como campos), HU-057/058/059
(atribuição rápida, prioridade no mapa, troca de equipe) e HU-030 (lista × cartões).

## 2. Decisões

### 2.1 Biblioteca de mapa: Leaflet 1.9.4 + react-leaflet 5.0.0, tiles do OpenStreetMap

* Sem chave de API nem cartão de crédito (Google Maps e Mapbox exigem) — coerente com a regra
  "nenhum grupo precisa contratar plano pago" da atividade.
* Bibliotecas maduras e mantidas; versões conferidas no npm e fixadas no `package.json`
  (`react-leaflet` 5 é a versão compatível com React 19).
* O desenho do polígono foi implementado com cliques no mapa (≈40 linhas), sem `leaflet-draw`,
  que está sem manutenção ativa.
* Atribuição "© OpenStreetMap" exibida no mapa, como pede a política de uso dos tiles. Para uso em
  produção real, trocar por um provedor de tiles contratado (a URL fica num único componente,
  `componentes/MapaBase.tsx`).

### 2.2 Seleção por polígono no navegador, sem PostGIS

* O C4 previa PostgreSQL + PostGIS. No Render/Neon gratuitos o GDAL complica o build e o ganho é
  pequeno: o mapa recebe só as OSs aptas de um polo (dezenas a poucos milhares).
* O teste `geometria.test.ts` mede 2.000 pontos bem abaixo de 1 s (HU-012 CA07).
* A regra continua no servidor: ao criar a rota, `roteirizar_ordens` revalida polo, estado e
  coordenada de cada OS (RN-08) e o banco garante, por `UNIQUE (ordem_servico)` em `ItemRota`,
  que a OS está em no máximo uma rota.
* As OSs de uma unidade dividem a coordenada da unidade (ERS §4: coordenadas são da unidade), por
  isso o mapa mostra um pin por unidade com a contagem.

### 2.3 Módulo `roteirizacao` e fronteira com o Núcleo

* O Roteirizador não muda o estado da OS diretamente: chama `nucleo.services_preparacao`
  (`roteirizar_ordens`, `despachar_ordens`), que passa pelo `CicloDeVidaOS` e grava a trilha.
* O `import-linter` ganhou o módulo nos três contratos (núcleo independente, módulos
  independentes, seeds isolados).

### 2.4 Arquivo RPA com layout proposto

* A dúvida bloqueante da HU-014 (layout oficial da automação) segue aberta. O grupo adotou CSV
  `;`, UTF-8, CRLF, uma linha por OS, e isolou o layout em `roteirizacao/arquivo_rpa.py`. Trocar
  pelo layout real muda só esse arquivo e o teste `test_ca06_layout...`.
* O conteúdo e o SHA-256 ficam no banco: "baixar novamente" devolve o mesmo arquivo (CA04) mesmo
  com o disco efêmero do Render.

## 3. Consequências

* **Positivas:** o fluxo principal do produto (importar → tratar → roteirizar → despachar) roda de
  ponta a ponta no protótipo; nenhuma conta paga nova.
* **Negativas / riscos aceitos:** sem PostGIS, consultas espaciais no servidor (ex.: "OSs a 500 m")
  exigirão migração futura; tiles públicos do OSM não servem para uso comercial intenso; layout RPA
  pode mudar quando a automação for definida.
