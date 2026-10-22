# ADR 0001 — Limite do frete grátis e arredondamento: preservar o comportamento atual

**Status:** aceita (AV2, refatoração de `calcular_total`). **Data:** 2026-10-21.

## Contexto
`calcular_total` diverge de `caso/regras.md` em dois pontos:
- **R1.3** — o código dá frete grátis com `total > 200`; o contrato diz `>= 200`. Subtotal 200,00 em PE: contrato 210,00, código 223,55.
- **R1.5** — o código usa `round()` sobre float; o contrato pede meio para cima. 0,20 em PE: contrato 13,76, código 13,75. Carrinho vazio em PE: contrato 13,55, código 13,54.

O teste antigo `test_cenarios_gravados` fixa 223,55 (`limite_200`) e 13,54 (`vazio`), isto é, o comportamento divergente.

## Decisão
A refatoração preserva o comportamento atual. O golden master (`caso/golden_calculo.json`, 2592 entradas, igualdade exata) o congela. As divergências viram `@unittest.expectedFailure` em `test_calculo_contrato.py`, com o esperado do contrato.

## Consequências
- O comportamento divergente continua em vigor neste caso didático.
- Se alguém corrigir, os `expectedFailure` acusam "unexpected success", e o golden e `test_cenarios_gravados` precisam ser revistos, em mudança **separada** da refatoração.

## Alternativa rejeitada
Corrigir junto com a refatoração: mistura estrutura com comportamento, e o golden deixaria de provar que nada mudou.

## Condição para rever
Decisão do dono do contrato de corrigir R1.3/R1.5. O impacto do carrinho vazio é baixo: R2.1 rejeita pedido sem itens antes do cálculo.
