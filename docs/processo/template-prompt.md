# Estrutura fixa de prompt

Todo pedido de código à IA segue estas cinco seções. Pedidos pequenos (um endpoint, um componente,
uma migration por vez) são mais fáceis de revisar.

```text
## Contexto
Projeto GeniOS (monólito modular Django + DRF / React + TS). Siga o guia AGENTS.md (colado abaixo
se a ferramenta não lê o repositório).
História: HU-XXX — <título>. Critérios de aceite: <colar CAs relevantes>.
Contrato: <colar o trecho do endpoint de docs/contrato-api.md>.
Modelo de dados envolvido: <tabelas de docs/banco/modelo-dados.md>.

## Tarefa
<uma única coisa: "Implementar o service registrar_saida_kit e seus testes">

## Critérios de qualidade
- Camadas do AGENTS.md §2 (sem regra na view, sem ORM fora de models/consultas/services)
- Limites do §4 (≤ 4 parâmetros, complexidade ≤ 8, funções curtas)
- Erros específicos herdando de ErroDeNegocio, formato {"erro": {...}} do contrato
- Um teste por critério de aceite, nome citando o CA

## Restrições
- Não adicionar dependências sem perguntar
- Não alterar o contrato da API nem migrations existentes
- Não usar except Exception; não usar dados reais

## Formato de saída
Apenas os arquivos criados/alterados, cada um com o caminho completo, seguidos de uma lista curta
das decisões tomadas e de dúvidas em aberto.
```

## Exemplo preenchido (Etapa 4)

```text
## Contexto
Projeto GeniOS, guia AGENTS.md. Histórias do MVP em docs/historias-priorizadas.md, contrato em
docs/contrato-api.md, diagrama de classes C4 nível 4 (Importacao, OrdemServico, Unidade, Polo,
RegistroAuditoria).

## Tarefa
Derivar os models Django e as migrations para as 5 histórias do MVP, mais um comando de seed com
dados fictícios.

## Critérios de qualidade
- Chave natural (numero, polo) da OS; estado com CHECK; auditoria append-only por trigger
- Índices para os filtros do contrato (polo + estado, abertura)
- Justificar cada decisão e listar riscos (consultas lentas, duplicidade)

## Restrições
- LGPD: só dados pessoais estritamente necessários
- Sem PostGIS no MVP (Render gratuito); nucleo não depende de módulos de negócio

## Formato de saída
models.py de cada app, migrations, comando de seed e uma tabela história → tabelas lidas/gravadas.
```
