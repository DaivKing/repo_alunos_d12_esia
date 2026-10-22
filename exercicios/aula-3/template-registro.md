# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.** Estudante: Davi Albnes — Data: 21/10/2026
Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: **execução própria** (Windows; `mutacao_manual.py` rodado com `MINILOJA_TEST_CMD` por falha do `shlex` com barras invertidas).


| Teste suspeito | Tipo de tautologia | Sabotagem que apliquei | Continuou verde? |
| --- | --- | --- | --- |
| `test_cupom_natal_com_flag` | sem asserção real (só `is not None`) | `0.8`→`0.79` (NATAL) em `calculo.py`; suíte `--existentes` | **Sim**: OK, 26 testes |
| `test_criar_pedido` | afirma o mock | `"status": "pago"`→`"xyz"` em `pedidos.py`; teste isolado e suíte | **Sim**: OK (1) e OK (26) |
| `test_cenarios_gravados` | snapshot do próprio código | `>`→`>=` (linha 46, `calculo.py`); teste isolado | **Não**, mas pelo motivo errado: obtido `limite_200: 210.0` ≠ gravado `223.55` |

Mutação (execução própria): 31 mutantes, 23 mortos, 8 sobreviventes, escore 74% (cobertura de linhas ~90% segundo o roteiro).

| Mutante sobrevivente | Por que sobreviveu | Teste que o matou |
| --- | --- | --- |
| `estoque.py`: `<`→`<=` | a suíte nunca reserva exatamente o saldo | `test_av13_estoque`: saldo 5, reservar 5 → aceita, saldo 0. Limpo OK / mutante FAILED (`EstoqueInsuficiente`) / limpo OK |
| `calculo.py`: NATAL 20%→21% | o único teste do NATAL só checa `is not None` | `test_av13_natal`: 300×1, NATAL, PE → **252,00**. Limpo OK / mutante FAILED (`248.85 != 252.0`) / limpo OK |

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão) | Observado | Decisão |
| --- | --- | --- | --- |
| 100×2, sem cupom, PE (fronteira do frete) | 200 ≥ 200 → frete 0; ×1,05 = **210,00** | 223,55 | código errado (R1.3: `>=`, código usa `>`) |
| 10×1, sem cupom, PE (arredondamento) | (10+12,90)×1,05 = 24,045 → **24,05** | 24,04 | código errado (R1.5, meio para cima; `round()` sobre float) |
| 210×1, `PROMO10`, PE | 189 < 200 → +12,90 = 201,90; ×1,05 = 211,995 → **212,00** | 212,0 | confere; não discrimina os erros acima |

**ADR curto:** contexto: 100,00×2 em PE (subtotal 200,00) devolveu 223,55 em vez de 210,00 (R1.3: frete grátis com subtotal com desconto ≥ 200), e o teste `limite_200` grava 223,55 ; decisão: o código está errado, `calcular_total` (linha 46) usa `total > 200` e deve usar `>= 200`; o contrato é o oráculo ; consequências: `limite_200` passa a falhar e seu esperado vira 210,00 (do contrato, não do código); rever se o dono da regra confirmar que 200,00 exato paga frete ; alternativa descartada: manter `>` e mudar o contrato, decisão que cabe ao dono da regra, não a quem lê o código.

**Trecho essencial de evidência:** `AssertionError: {'limite_200': 210.0, ...} != {'limite_200': 223.55, ...}` (sabotagem 3). **Limite do que a suíte garante:** mesmo com os 2 testes novos, seguem sem cobertura os sobreviventes restantes (frete RJ, percentual do VIP15, e-mail obrigatório, total formatado, relatório); um deles é equivalente (variável sem efeito). O arredondamento meio para cima continua divergente (24,04 vs 24,05) e não foi corrigido. Rever a decisão do ADR se o contrato mudar.

**Procedência/IA:** **Procedência/IA:** ferramenta: Claude Code, modelo não informado; tarefa delegada: aplicar cada sabotagem/mutante, rodar a suíte e restaurar; trecho aproveitado: comandos e saídas das execuções, redação do ADR após minha revisão ; minha verificação/intervenção: calculei os três esperados à mão antes de ver o código, escolhi os testes e mutantes e decidi qual lado estava errado. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] três testes; [x] dois mutantes; [x] três casos do contrato; [x] ADR; [x] até uma página.
