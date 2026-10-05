# Lacunas da ERS — propostas para validação do grupo

> Status: **proposta — validar com o grupo**. Nada aqui altera a ERS até o grupo aprovar.
> Fontes: `docs/requisitos/ers.md` e o protótipo de design (`GeniOS ERP.html`).

A ERS cobre bem o fluxo, mas há ações citadas em regras de negócio, RNFs, no ciclo de vida da OS
ou no protótipo que **não têm requisito funcional**. Em desenvolvimento orientado a especificação,
o que não está especificado é inventado pelo agente — por isso cada lacuna abaixo vira um RF
proposto e uma história de usuário marcada como proposta.

## 1. Requisitos funcionais propostos

| RF proposto | Descrição | Por que existe | Evidência | HU |
|---|---|---|---|---|
| RF-ROT-03 | Criar rota com nome, cor, data, previsão de início, carregamento, equipe/veículo, profissional, ajudante e observação, a partir das OSs selecionadas | O fluxo vai de "selecionar por polígono" (RF-ROT-07) direto para "finalizar" (RF-ROT-16); não há como criar a rota | Modal "Criar Rota" do protótipo; entidade Rota (ERS §4) | HU-056 |
| RF-ROT-04 | Atribuir despacho: vincular OSs selecionadas a uma equipe em uma data | Estado 5 "Roteirizada" exige equipe e data (ERS §2.4) | Modal "Atribuir despacho" | HU-057 |
| RF-ROT-05 | Marcar OS como prioridade a partir do mapa | RN-02 cita prioridade tratada manualmente, mas nenhum RF a define | Ação "Marcar como prioridade" no pin | HU-058 |
| RF-ROT-06 | Trocar serviço ou equipe de OS roteirizada, antes do despacho | RN-10 bloqueia edição só **após** o RPA, implicando que antes é permitida | Ação "Trocar serviço / equipe" no pin | HU-059 |
| RF-PEN-06 | Concluir o tratamento de uma pendência, levando a OS a "Apta a roteirizar" | Transição 2→4 do ciclo de vida não tem dono nem critério | ERS §2.4 | HU-060 |
| RF-ALM-06 | Liberar excepcionalmente a trava de histórico, com justificativa | RN-13 e RNF-12 citam a liberação; não há RF (e o número 06 está vago na ERS) | ERS §6.3 | HU-063 |
| RF-ALM-11 | Registrar envio de kits para outro polo | RF-ALM-07 lista envios pendentes, mas nada cria um envio | Painel "Envios pendentes" | HU-067 |
| RF-AUD-06 | Listar as invalidações da fiscalização da concessionária | Estado 8 "Invalidada" e a entidade Invalidação existem, sem RF | Aba "Invalidações" (fiscalização CAGEPA) | HU-061 |
| RF-AUD-07 | Forçar validação de OS invalidada, por perfil autorizado e com justificativa | RN-14, RNF-12 e o perfil Gerente de Contrato citam a ação | Botão "Forçar validação" | HU-062 |
| RF-AUD-08 | Fechar e reabrir o ciclo de medição, levando as OSs validadas a "Faturada" | RN-15 cita reabertura; estado 10 "Faturada" não tem transição definida | ERS §2.4, RN-15, RN-19 | HU-064 |
| RF-TRV-06 | Gerenciar usuários, perfis e polos de acesso | O perfil Administrador "cadastra usuários e perfis" (ERS §2.2) sem RF | ERS §2.2 | HU-065 |
| RF-TRV-07 | Parametrizar tabela de preços, prazos contratuais, unidades do escopo, operações e vínculo kit ↔ tipo de serviço | RNF-27 exige parametrização; RF-IMP-03, RN-06, RN-11 e RN-16 dependem desses parâmetros | ERS §6.7, PR-04 | HU-066 |
| RF-GER-06 *(desejável)* | Exibir ranking de equipes por produção validada | Aparece no protótipo, ausente na ERS | Card "Ranking de equipes" | HU-068 |

## 2. RNFs que precisam de número para serem verificáveis

| RNF | Problema | Proposta |
|---|---|---|
| RNF-03 | "sem degradação perceptível" não é medível | Com 2.000 pins, concluir a seleção por polígono e atualizar o contador em até 1 s |
| RNF-11 | Política de senha e tempo de inatividade não definidos | Senha ≥ 10 caracteres com letras e números; sessão expira após 30 min de inatividade |
| RNF-14 | "mínimo necessário" não é verificável | Endereço/imóvel visível apenas para perfis com acesso ao polo da OS (ver RN-20) |
| RNF-16 | Vigência do contrato não informada | Retenção mínima de 5 anos até a vigência ser informada |
| RF-ASS-* | Sem tempo de resposta do assistente | Primeira resposta do assistente em até 10 s |

## 3. Ambiguidades em regras de negócio

| Regra | Pergunta |
|---|---|
| RN-11 (trava) | "D−1" é o dia anterior corrido ou o último dia útil com execução? A trava compara cada saída ou a **soma** das saídas do dia? Sem execução anterior (primeiro dia, segunda-feira), a saída é bloqueada? |
| RN-11 (trava) | Como se obtém a "quantidade executada por kit"? A execução vem por tipo de serviço (planilha de execução); falta o vínculo kit ↔ tipo de serviço (RF-TRV-07 proposto). |
| RN-06 (atraso) | O prazo conta horas corridas ou só horário operacional? |
| RF-IMP-01 | 25 MB = 25 × 1.000.000 ou 25 × 1.048.576 bytes? |
| RF-IMP-03 | Onde fica a lista de "unidades do escopo contratual"? (RF-TRV-07 proposto) |
| RN-01 × RN-03 | A chave do upsert inclui o Polo, mas a planilha GSAN traz a Unidade; o polo é derivado do cadastro da unidade? |

## 4. Faseamento × dependências

A ERS põe o Almoxarifado (Fase 4) depois da Auditoria (Fase 3), o que é coerente: a trava de
histórico (RN-11) depende da execução do dia anterior, que só existe após a importação da
planilha de execução (RF-AUD-01). Manter essa ordem.
