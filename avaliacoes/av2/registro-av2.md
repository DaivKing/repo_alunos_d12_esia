# Registro individual — AV2

**Limite: duas páginas de análise + anexo técnico curto.** Estudante: ___ — Data: 21/10/2026 — Caminho: B (MiniLoja)

**Escopo (seis campos):** objetivo: refatorar `calcular_total` (`caso/miniloja/calculo.py`) para ficar legível (tabelas `FRETE_POR_UF`/`TAXA_POR_UF`, sem código morto nem comentário obsoleto, docstring com o contrato) sem mudar nenhum resultado; pode tocar: só `caso/miniloja/calculo.py`; pode criar: `caso/golden_master.py`, `caso/golden_calculo.json`, `caso/testes_existentes/test_golden_calculo.py`, `caso/testes_existentes/test_calculo_contrato.py`, `caso/adr/0001-...md`, `avaliacoes/av2/registro-av2.md` e `avaliacoes/av2/evidencias/`; não pode tocar: `testes/`, `caso/regras.md`, os testes antigos de `caso/testes_existentes/`, outros módulos de `caso/miniloja/` e o `golden_calculo.json` depois de gerado; invariantes: assinatura `calcular_total(itens, cupom=None, uf="PE")`, retorno float com igualdade exata no golden, laço simples no subtotal (sem `sum()`), ordem desconto → frete → taxa, flag NATAL lida a cada chamada, testes existentes verdes, verificações em 8 ok / 3 falhas (v08–v10); pronto quando: golden 100% igual, suíte verde, verificações inalteradas, mutação rodada antes (e sabotagens depois); pare e pergunte se: o golden acusar diferença, algo parecer bug (reportar, não corrigir), for preciso tocar arquivo fora do escopo ou algo falhar diferente da linha de base.

**Plano do agente: o que cortei ou corrigi:**
(a) O agente propôs não testar as divergências do contrato. Exigi `@unittest.expectedFailure` com o esperado do contrato (3 casos, ver ADR 0001).
(b) Propôs copiar a ferramenta de mutação ou deformar o código para casar com ela. Reordenei: mutação com os testes novos **antes** da refatoração, com a ferramenta oficial; depois, golden e sabotagens manuais.
(c) Pedi golden e testes de contrato em arquivos separados e a mutação com e sem golden, para o snapshot não inflar o escore.

**Comportamento preservado:** método: golden master gerado do código **original** (`caso/golden_master.py --gerar`) e comparado com `==` e `type is float`; entradas: 2592 (carrinhos × 8 cupons × 6 UFs × 3 estados da flag NATAL, incluindo subtotais 199,99, 200,00 e 200,01, carrinho vazio e centavos); resultado: `python -B caso/golden_master.py --comparar` → "entradas: 2592 | iguais: 2592 | diferentes: 0" no código original (`01-golden-original.txt`), após cada um dos 4 passos (`05-refatoracao-passos.txt`) e no final (`05-golden-pos-refatoracao.txt`). Suíte `--existentes`: 46 testes, OK, 3 expected failures (`08-suite-final.txt`); verificações: 8 ok / 3 falhas, v08–v10 (`07-final.txt`).

| Teste (derivado de qual regra do contrato) | Como provei que falharia (sabotagem, mutação ou diferencial) | Resultado |
| --- | --- | --- |
| `test_r1_3_4_rj_frete_21_50_taxa_6_por_cento` (R1.3, R1.4) | Sabotagem `"RJ": 21.5` → `22.5` na tabela; o mutante "frete RJ" sobrevivia à suíte antiga (`00-mutacao-base.txt`) | 7 falhas, incluindo este (`06-sabotagens.txt`); mutante morto em `04a` |
| `test_r1_2_natal_com_campanha_ativa_desconta_20_por_cento` e `..._le_a_campanha_a_cada_chamada` (R1.2) | O mutante "NATAL: 20% → 21%" sobrevivia (`00`) | Morto com os testes novos (`04a`) e sem o golden (`04b`) |
| `test_r1_2_promo10_desconta_10_por_cento` (R1.2) | Sabotagem `0.9` → `0.91` | 5 falhas, incluindo este (`06`) |
| `test_r1_3_4_sp_frete_19_90_taxa_7_por_cento` (R1.3, R1.4) | Sabotagem taxa SP `0.07` → `0.08` | 10 falhas, incluindo este (`06`) |
| `test_r1_3_acima_do_limite_nao_paga_frete` e `test_r1_6_desconto_que_derruba...` (R1.3, R1.6) | Sabotagem `total > 200` → `total > 300` | 6 falhas, incluindo ambos (`06`) |
| 3 `expectedFailure` (R1.3 limite 200,00; R1.5 0,20 e vazio em PE) | O esperado vem do contrato; falham no código atual ("expected failure", `08`). Se alguém corrigir o código, viram "unexpected success" | 3 expected failures (`08-suite-final.txt`) |

**Mutantes sobreviventes e tratamento (ou equivalentes justificados):** mutação oficial: 74% (23/31) na base (`00`) → 81% (25/31) com os testes novos (`04a`) e **igual sem o golden** (`04b`; comando: `MINILOJA_TEST_CMD='python -B -m unittest discover -f -s caso/testes_existentes -t caso -p "test_[!g]*.py"' python -B testes/mutacao_manual.py`). Em `calculo.py` resta só `desconto_aplicado = True` → `False`: **equivalente**, pois a variável só alimentava um `if desconto_aplicado: pass` e foi removida no passo 2 da refatoração. Os 5 sobreviventes de outros módulos (`descontos.py` VIP15, `estoque.py` limite, `cadastro.py` e-mail, `pedidos.py` total formatado, `relatorios.py` formatação) ficam **fora do escopo**, sem teste: limite. A mutação não foi rodada depois da refatoração (as âncoras de texto da ferramenta sumiram); foi substituída pelas 4 sabotagens acima.
**Documentação (contrato e motivo) ou ADR:** docstring de `calcular_total` com argumentos, ordem, retorno e divergências conhecidas; `caso/adr/0001-limite-frete-e-arredondamento.md` (contexto com números reais, decisão de preservar, consequências, alternativa rejeitada, condição para rever).
**O que a IA errou (o quê, onde, como detectei):**
1. Plano: "não assertar a divergência" deixaria o bug invisível; detectado na revisão do plano.
2. Plano: afirmou "o golden vale mais que regras.md", o inverso do CLAUDE.md ("o contrato vale mais que o código"). O golden protege a refatoração; o esperado dos testes vem do contrato. Detectado na revisão.
3. Execução, passo 2: o script de edição abortou num assert e o script de passo commitou só a evidência (commit `7d6555b`, 1 arquivo, 8 linhas), registrando um passo que não aconteceu. Visível em `git reflog` e `git show --stat 7d6555b` (`09-ambiente-e-reflog.txt`). Desfeito com `git reset --soft HEAD~1` (reflog `HEAD@{6}`); apaguei o registro falso e refiz o passo (`64d5f4c`).
4. Refatoração: `.get(uf, padrão)` muda o comportamento para `uf` não hashável (`TypeError` em vez da UF padrão); o golden não cobre. Decisão: não corrigir, fora do domínio do contrato; registrado aqui.
**Limite da verificação e condição para rever:** o golden cobre só a grade gerada (`uf` string, preços da grade); float e `round` dependem da plataforma (rodado em Python 3.15.0, `09-ambiente-e-reflog.txt`; confirmado em 3.10 numa verificação independente, abaixo do 3.11 exigido, informada pelo estudante, sem arquivo de evidência); mutação não rodada pós-refatoração (âncoras sumiram) → 4 sabotagens manuais; `mutacao_manual.py` quebra no Windows por `shlex.split(sys.executable)` (`FileNotFoundError`), contornado com `MINILOJA_TEST_CMD` (`00`); mutantes de outros módulos não tratados. Rever se o dono do contrato decidir corrigir R1.3/R1.5 ou se mudar a plataforma ou a versão do Python.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, modelo ___; Claude (chat), modelo ___, usado para planejar o escopo e revisar o plano; tarefa delegada e contexto: ___; trecho aproveitado: ___; minha verificação/intervenção: ___. O raciocínio e a decisão registrados são meus.

**Anexo:** resumo do diff — `git diff main --stat -- . ":!caso/golden_calculo.json"` (o JSON tem 34.706 linhas geradas; estado antes do commit deste registro):
```
 avaliacoes/av2/evidencias/00-mutacao-base.txt      |  12 ++
 avaliacoes/av2/evidencias/01-golden-original.txt   |   5 +
 avaliacoes/av2/evidencias/03-suite-com-novos.txt   |  52 ++++++++
 .../av2/evidencias/04a-mutacao-com-golden.txt      |   9 ++
 .../av2/evidencias/04b-mutacao-sem-golden.txt      |   9 ++
 .../av2/evidencias/05-golden-pos-refatoracao.txt   |   7 ++
 .../av2/evidencias/05-refatoracao-passos.txt       |  32 +++++
 avaliacoes/av2/evidencias/06-sabotagens.txt        |  44 +++++++
 avaliacoes/av2/evidencias/07-final.txt             |  43 +++++++
 avaliacoes/av2/evidencias/08-suite-final.txt       |  56 +++++++++
 avaliacoes/av2/evidencias/09-ambiente-e-reflog.txt |  22 ++++
 caso/adr/0001-limite-frete-e-arredondamento.md     |  23 ++++
 caso/golden_master.py                              | 102 ++++++++++++++++
 caso/miniloja/calculo.py                           |  80 +++++-------
 caso/testes_existentes/test_calculo_contrato.py    | 135 +++++++++++++++++++++
 caso/testes_existentes/test_golden_calculo.py      |  33 +++++
 16 files changed, 617 insertions(+), 47 deletions(-)
```
`calculo.py`: +33 −47. Docstring com contrato; remove o comentário de 2023, `desconto_aplicado` e o `if ...: pass`; `FRETE_POR_UF.get(uf, FRETE_PADRAO)` e `TAXA_POR_UF.get(uf, TAXA_PADRAO)` no lugar das cadeias `if/elif`; cadeia de cupom plana (`elif cupom == "NATAL" and flags.promo_natal_ativa()`); laço do subtotal, ordem e `round(total, 2)` intactos.
Trechos dos testes (`test_calculo_contrato.py`):
```python
def test_r1_2_promo10_desconta_10_por_cento(self):
    # 100 * 0,90 = 90; SP: (90 + 19,90) * 1,07 = 117,593 -> 117,59
    self.assertEqual(calcular_total(CEM, "PROMO10", "SP"), 117.59)

@unittest.expectedFailure
def test_r1_3_subtotal_exatamente_200_tem_frete_gratis(self):
    # Divergência R1.3 — reportada, não corrigida; ver ADR 0001.
    # O código usa "total > 200"; o contrato diz "maior ou igual a R$ 200,00".
    # 200 >= 200, sem frete; PE: 200 * 1,05 = 210,00 (o código devolve 223,55)
    self.assertEqual(calcular_total([{"preco": 200.0, "qtd": 1}], None, "PE"), 210.0)

def test_r1_2_natal_le_a_campanha_a_cada_chamada(self):
    os.environ["MINILOJA_PROMO_NATAL"] = "1"
    ligada = calcular_total(CEM, "NATAL", "RJ")  # 107,59
    os.environ["MINILOJA_PROMO_NATAL"] = "0"
    desligada = calcular_total(CEM, "NATAL", "RJ")  # 128,79
    os.environ["MINILOJA_PROMO_NATAL"] = "1"
    religada = calcular_total(CEM, "NATAL", "RJ")  # 107,59
    self.assertEqual((ligada, desligada, religada), (107.59, 128.79, 107.59))
```
**Revisão:** [ ] escopo; [ ] comportamento; [ ] testes com prova; [ ] documentação; [ ] erros da IA; [ ] limite.
