---
id: HU-015
titulo: Registrar a saída de kits para uma equipe
ordem: 67
modulo: Almoxarifado
epico: EP-C Suprimentos e logística
tela: "Almoxarifado" › "Saída de kit"
fase: 4
prioridade: MVP
status: rascunho
requisitos: [RF-ALM-01]
regras: [RN-11]
nao_funcionais: [RNF-08, RNF-15]
depende_de: [HU-009, HU-032, HU-054]
---

# HU-015 — Registrar a saída de kits para uma equipe

## História
Como **Almoxarife**, quero **registrar quantos kits de cada tipo entreguei a cada equipe**, para
**que o saldo do almoxarifado do polo fique correto**.

## Regras de negócio
- **RN-L01** — Campos: polo (vem do seletor), equipe (ativa, do polo), tipo de kit (ativo),
  quantidade (inteiro ≥ 1). Todos obrigatórios.
- **RN-L02** — A quantidade não pode ser maior que o saldo disponível do polo.
- **RN-L03** — Antes de registrar, aplica a trava de histórico (HU-016).
- **RN-L04** — Registro guarda data/hora e usuário; saldo do polo diminui na mesma operação.
- **RN-L05** — Com "Todos" no seletor, a saída fica bloqueada (ERS §2.3).

## Critérios de aceite
CA01 — Registrar
Dado o Polo 1 com saldo de 40 "Kit Ligação Simples" e trava liberando 15
Quando registro 10 para a Equipe A
Então a saída é gravada com data/hora e usuário, o saldo passa a 30 e aparece o toast
"Saída registrada: 10 Kit Ligação Simples → Equipe A".

CA02 — Saldo insuficiente
Dado saldo de 5
Quando registro 10
Então aparece "Saldo insuficiente: 5 un. disponíveis no Polo 1" e nada é gravado.

CA03 — Campos obrigatórios
Dado equipe não escolhida ou quantidade 0
Quando clico em "Registrar saída"
Então o campo é destacado com o motivo.

CA04 — Polo "Todos"
Dado o seletor em "Todos"
Quando abro a saída de kit
Então o formulário está desabilitado com "Selecione um polo".

CA05 — Equipe de outro polo pela API
Dado o Polo 1
Quando envio à API uma saída para equipe do Polo 2
Então recebo `422`.
