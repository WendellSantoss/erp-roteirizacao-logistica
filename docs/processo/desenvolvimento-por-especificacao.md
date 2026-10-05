# Como vamos desenvolver o GeniOS: desenvolvimento orientado a especificação

> Para: Ana, Felipe, Wendell e Deivisson. Leitura de ~10 minutos.

## 1. A ideia em uma frase

**A IA escreve o código; nós escrevemos e revisamos o que ela deve fazer.** O código sai de uma
especificação aprovada pelo grupo, e não de um pedido solto no chat.

## 2. Por que trabalhar assim

Um agente de IA (Claude Code, Codex, Copilot) programa rápido, mas **preenche sozinho tudo o
que não foi dito**. Se a história diz só "o sistema deve bloquear a saída acima do limite", o
agente vai inventar qual é o limite, o que acontece no domingo e o que fazer com duas saídas ao
mesmo tempo — e cada vez que alguém pedir, vai inventar diferente.

Por isso o esforço do grupo muda de lugar:

| Antes | Agora |
|---|---|
| Escrever código | Escrever e revisar **especificações** |
| Descobrir o comportamento testando | O comportamento está nos **critérios de aceite** antes do código |
| Revisar código linha a linha | Revisar se o código **cumpre a spec** e se **cada critério tem teste** |

Bônus para a disciplina: cada decisão fica registrada (história → spec → PR), o que é exatamente
a rastreabilidade que o projeto arquitetural pede.

## 3. Onde fica cada coisa

```
docs/
├── requisitos/
│   ├── ers.md              ← a ERS do grupo (fonte dos RF, RN e RNF)
│   └── lacunas.md          ← o que falta na ERS e o que propusemos
├── historias/
│   ├── README.md           ← modelo, regras, ORDEM DE DESENVOLVIMENTO, índice
│   ├── RASTREABILIDADE.md  ← qual RF/RN/RNF está em qual história
│   ├── fundacao/           ← HU-F01…F13: setup do projeto
│   └── HU-xxx-*.md         ← uma história por arquivo
├── specs/
│   └── HU-xxx/
│       ├── spec.md         ← COMO a história será implementada
│       └── plano.md        ← tarefas pequenas para o agente executar
├── design/prototipo/       ← o protótipo das telas
└── processo/               ← este documento
AGENTS.md                   ← regras do projeto que todo agente lê (criado na HU-F07)
```

**O arquivo no repositório é a fonte da verdade.** A issue no GitHub Project é uma cópia para
acompanhamento. Mudou a história? Muda o arquivo, por pull request.

## 4. Os três documentos de cada história

| Documento | Responde | Quem escreve | Quem aprova |
|---|---|---|---|
| **História** (`docs/historias/HU-xxx.md`) | **O quê** e **por quê**: regras de negócio e critérios de aceite em Dado/Quando/Então | Grupo (já estão escritas) | Grupo |
| **Spec** (`docs/specs/HU-xxx/spec.md`) | **Como**: modelo de dados, endpoints, telas, testes, riscos | Dev com o agente | Outra pessoa do grupo |
| **Plano** (`docs/specs/HU-xxx/plano.md`) | **Em que passos**: tarefas pequenas (≤ 5 arquivos cada), cada uma com seu teste | Dev com o agente | Quem escreveu a spec |

## 5. O fluxo de uma história, passo a passo

```
 1. Pegar a próxima       2. Está pronta?        3. Spec           4. Revisão da spec
    (campo Ordem)   →        (Definição de   →     (dev + IA)   →     (outra pessoa)
                              Pronta)                                       │
                                                                            ▼
 8. Concluída      ←   7. Homologação    ←   6. Pull request   ←   5. Plano + código
                          (testar os CAs)       (CI + revisão)          (dev + IA, teste
                                                                         antes do código)
```

1. **Pegar a próxima história pela ordem.** No Project, ordenar pelo campo **Ordem**. A ordem já
   respeita as dependências — não pule. Mova a issue para "em desenvolvimento" e atribua a você.
2. **Conferir se ela está pronta** (checklist "Definição de Pronta" no `docs/historias/README.md`).
   Se tem **dúvida em aberto que muda o comportamento**, ela **não** vai para o agente: a dúvida
   vai para quem faz a ponte com o cliente (ver papéis).
3. **Gerar a spec com o agente** (prompt na seção 8). O agente lê a história, o `AGENTS.md`, a ERS
   e o protótipo, e propõe o "como". Você lê e corrige antes de mostrar para alguém.
4. **Revisão da spec por outra pessoa do grupo.** Esse é o ponto de controle mais importante:
   errar aqui é barato; errar depois do código é caro. Pode ser feita por quem não programa —
   a pergunta é "isso cumpre a história e os critérios?".
5. **Plano e código.** O agente quebra a spec em tarefas e implementa **uma de cada vez**,
   escrevendo primeiro o teste do critério de aceite (que falha) e depois o código (que faz
   passar). Nome do teste com o ID: `test_hu016_ca02_bloqueia_acima_da_execucao`.
6. **Pull request.** Um PR por história, citando `HU-xxx` no título. O CI roda lint e testes; o
   merge só sai com CI verde **e** aprovação de outra pessoa.
7. **Homologação.** Após o merge, a versão sobe sozinha para o ambiente de homologação (HU-F10).
   Alguém que **não** escreveu o código testa cada critério de aceite na tela.
8. **Concluída.** Issue fechada, status atualizado.

## 6. Papéis

Hoje, quem tem acesso a agente de código é o Deivisson e o Felipe. Isso não significa que só eles
trabalham: no desenvolvimento com IA, revisar e testar vale tanto quanto programar.

| Papel | Quem | O que faz |
|---|---|---|
| **Desenvolvedor com agente** | Deivisson, Felipe | Passos 3, 5 e 6: gera spec, plano e código com o agente, abre os PRs |
| **Revisor de spec e PR** | Ana, Wendell (e os devs se revisam entre si) | Passo 4 e revisão do passo 6: confere se a spec e o PR cumprem a história e se cada critério tem teste |
| **Homologação / QA** | Ana, Wendell | Passo 7: testa os critérios de aceite na tela e abre issue de bug quando falhar |
| **Ponte com o cliente / dono do produto** | A definir no grupo | Leva as "dúvidas em aberto" ao cliente e atualiza as histórias com a resposta |
| **Arquitetura e documentação** | Grupo (C4, ADR) | Mantém o C4 e os ADRs alinhados com o que foi implementado |
| **Dono do repositório** | Wendell | Proteção da `main`, permissões, configurações do GitHub |

Os papéis podem mudar. Se a Ana ou o Wendell tiverem acesso a um agente (ver seção 9), viram
desenvolvedores também.

## 7. Regras de ouro

1. **Nenhum código sem história.** Se não tem HU, cria-se a HU primeiro.
2. **Nenhum código sem spec aprovada por outra pessoa.**
3. **Cada critério de aceite tem pelo menos um teste automatizado.**
4. **Um PR = uma história.** PR pequeno é revisado; PR gigante é aprovado sem ler.
5. **O agente não decide regra de negócio.** Se ele perguntar ou "supor" algo que não está na
   história, isso é uma dúvida para o grupo, não uma decisão dele.
6. **Revisar tudo o que a IA gerou.** Quem abre o PR responde pelo código, mesmo que não tenha
   digitado.
7. **Nunca colar dados reais** (planilha do GSAN, endereços, nomes) no agente. Use os dados
   fictícios da HU-F09 (LGPD, RNF-14).
8. **Não editar a história no meio da implementação sem avisar.** Mudou a regra? Atualize o
   arquivo, avise no grupo e reveja a spec.

## 8. Prompts modelo

Os agentes leem o `AGENTS.md` sozinhos, então os prompts podem ser curtos.

**Gerar a spec**
```
Leia docs/historias/HU-016-trava-de-historico.md, a ERS em docs/requisitos/ers.md e a tela
correspondente em docs/design/prototipo/. Escreva docs/specs/HU-016/spec.md usando o modelo
docs/specs/_modelos/spec.md. Não invente regra de negócio: se algo não estiver na história,
liste em "Perguntas" em vez de decidir.
```

**Gerar o plano**
```
A spec docs/specs/HU-016/spec.md foi aprovada. Escreva docs/specs/HU-016/plano.md com tarefas
de no máximo 5 arquivos cada, cada uma com o teste que a comprova.
```

**Implementar**
```
Execute a tarefa 1 de docs/specs/HU-016/plano.md. Escreva primeiro o teste do critério de
aceite e confirme que ele falha; depois implemente o mínimo para passar. Rode lint e testes.
```

**Revisar (útil para quem revisa PR, com qualquer chat de IA)**
```
Aqui estão a história, a spec e o diff do PR. Para cada critério de aceite, diga se há teste
que o cobre e se o código o cumpre. Aponte qualquer regra implementada que não esteja na história.
```

## 9. Ferramentas e custo

| Ferramenta | Como funciona | Custo (aprox., conferir antes de assinar) |
|---|---|---|
| **Claude Code** | Agente no terminal/VS Code | Exige plano pago da Anthropic (Pro, cerca de US$ 20/mês) ou uso pago da API |
| **Codex (OpenAI)** | Agente no terminal/VS Code/web | Incluído nos planos pagos do ChatGPT (Plus, cerca de US$ 20/mês) |
| **GitHub Copilot** | Agente no VS Code | **Gratuito para estudantes** pelo GitHub Student Developer Pack (verificar elegibilidade) |

Claude Code e Codex leem as mesmas regras (`AGENTS.md`; o `CLAUDE.md` só importa esse arquivo),
então dá para misturar ferramentas no grupo sem que cada um programe de um jeito.

Para **revisar** spec e PR não é preciso agente de código: qualquer chat de IA gratuito ajuda,
usando o prompt de revisão da seção 8.

## 10. Status de uma história no Project

`rascunho` → `pronta` → `em desenvolvimento` → `em revisão` → `concluída`

- **rascunho**: tem dúvida em aberto que muda o comportamento.
- **proposta**: história nova que cobre lacuna da ERS — o grupo precisa aprovar antes.
- **pronta**: passou na Definição de Pronta; pode ir para o agente.

## 11. Por onde começamos

1. **Grupo:** validar as 13 histórias marcadas como `proposta` e definir quem faz a ponte com o cliente.
2. **Ponte com o cliente:** levar as dúvidas bloqueantes — layout do arquivo RPA (HU-014), planilha
   GSAN real anonimizada (HU-002), coluna de reprovação da planilha de execução (HU-018), acesso
   ao portal GSAN (HU-005) e o "dia anterior" da trava (HU-016).
3. **Devs:** histórias de ordem 1 a 13 (fundação: monorepo, Docker, esqueletos, CI, `AGENTS.md`…).
   Elas não dependem das dúvidas acima.
4. **Wendell:** proteger a `main` (exigir PR com 1 aprovação) — critério CA05 da HU-F01.
