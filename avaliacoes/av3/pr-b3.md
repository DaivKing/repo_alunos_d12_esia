# B3: desfazer reservas de estoque quando um item falha (R2.2)

> **Aviso para quem revisa:** os commits `fa52a97` e `8bec5f7` são **insumos** (registros e golden master do `calcular_total`), não fazem parte da mudança. A revisão do código começa em `f1254ad`: `git diff 8bec5f7..HEAD -- caso/`. A mensagem do `8bec5f7` diz "(AV2)" por engano: o golden de 64 cenários vem da AV1.2 (branch `tarefa/r2`); ver o registro de erros.

## Intenção e escopo
Corrigir R2.2 (`caso/regras.md`): se algum item do pedido não tem estoque, o pedido é recusado (409) e **nenhuma reserva pode permanecer**. Hoje `PedidoService.criar` reservava item a item e, se o item N falhava, as reservas dos itens 1..N-1 ficavam (saldo decrementado, entradas em `reservas`).

- **Pode tocar:** `caso/miniloja/pedidos.py`, `caso/miniloja/estoque.py`, novo `caso/testes_existentes/test_reserva_estoque.py`, `.txt` em `avaliacoes/av3/evidencias/`.
- **Não toca:** `testes/`, `caso/regras.md`, testes existentes e golden, demais módulos, `exercicios/`, `avaliacoes/av2/`. Sem dependências novas.
- **Invariantes:** assinaturas de `criar` e `reservar`; `EstoqueInsuficiente` com o SKU que faltou; pedido bem-sucedido igual a hoje; sem cobrança nem pedido salvo na falta de estoque. R2.3 (pagamento recusado) fora do escopo.
- **Barreira:** `06` (código e evidências 00–05) e `09`, final, gerada depois do último commit de conteúdo. Os arquivos de documentação (`pr-b3.md`, `plano-b3.txt`, `template-registro.md`) são entrega, fora do escopo de código; esse desvio está declarado no registro.

## Plano
[`avaliacoes/av3/plano-b3.txt`](plano-b3.txt) (plano original do agente, em modo plano, antes da revisão). Corrigido na revisão:
1. Risco 3: o agente recomendava `except Exception` por supor `KeyError` de item sem `qtd`; `calculo.py:14` lê `i["qtd"]` antes do laço. Captura só `EstoqueInsuficiente`. A preocupação de fundo vale para item sem `sku` (evidência 08), que não é R2.2 e fica nos limites.
2. Passo 6: sabotagem "comentar o `except`" poderia dar `SyntaxError` (ERROR, não FAIL). Trocado por `pass` no corpo do laço de liberação.
3. Seção 3: o caso (c) afirmava as chaves `tmp-1` como se fossem contrato. Ganhou comentário de caracterização.

## Mudança
- `estoque.py`: novo `Estoque.liberar(sku, qtd, pedido_id)`: devolve `qtd` ao saldo e abate a entrada em `reservas` (remove a chave quando chega a zero ou menos; tolera chave ausente). `reservar` não mudou.
- `pedidos.py`: `criar` guarda `feitas` (SKU, qtd de cada reserva bem-sucedida). Em `EstoqueInsuficiente`, libera `feitas` em **ordem reversa** e **relança** a mesma exceção. O saldo volta pela soma exata do que foi reservado, não pelo valor em `reservas`, que é sobrescrito com SKU repetido (chave `(pedido_id, sku)`).

Commits: `f1254ad` linha de base · `446115c` teste novo (falha esperada) · `0e6d253` `Estoque.liberar` · `8989a2a` correção em `criar` · `6294841` evidências 03 a 05 · `9761891` barreira 06. O histórico fica vermelho em `446115c` de propósito.

## Como foi verificado
Windows, `python -B`, Python 3.15 (conferido com `python --version` depois da execução; não capturado nas evidências 00–07).

| Evidência | Comando | Resultado |
| --- | --- | --- |
| 00 linha de base | `python -B testes/test_miniloja.py --codigo caso` e `... --existentes` | 8 ok / 3 falhas (v08, v09, v10); suíte existente 27 OK |
| 01 teste novo falha | `python -B -m unittest discover -s caso/testes_existentes -t caso -p "test_reserva_estoque.py" -v` e suíte completa | (a), (b), (b2) FALHAM por asserção; (c) passa; 31 testes, `failures=3`, `LASTEXITCODE=1` |
| 02 teste novo passa | mesmos comandos após a correção | 4 OK; suíte 31 OK, `LASTEXITCODE=0` |
| 03 sabotagem do desfazer | corpo do laço de liberação trocado por `pass` | (a), (b), (b2) falham por asserção; (c) passa; restaurado com `git checkout`, `git diff --stat` vazio |
| 04 verificações oficiais | `python -B testes/test_miniloja.py --codigo caso` | 8 ok / 3 falhas (v08, v09, v10), igual à base; `LASTEXITCODE=1` |
| 05 suíte existente | `python -B testes/test_miniloja.py --codigo caso --existentes` | 31 testes OK (27 + 4 novos) |
| 06 barreira de escopo | `git diff --name-only 8bec5f7..HEAD` | só arquivos permitidos; fora do escopo: vazio |
| 07 sabotagem da armadilha | desfazer via `self.estoque.reservas` em vez de `reversed(feitas)`; `python -B -m unittest discover -s caso/testes_existentes -t caso -p "test_reserva_estoque.py" -v` | só `test_sku_repetido_restaura_saldo_exato` falha (`8 != 10`); os outros 3 passam; `LASTEXITCODE=1`; restaurado, `git diff --stat` vazio |
| 08 limite: item sem `sku` | trecho Python do passo 2, dentro de `caso/` (`python -B -c`) | `KeyError 'sku'`; saldo 8; a reserva `('tmp-1', 'BOLA-01'): 2` fica; fora de R2.2 |
| 09 barreira final | `git diff --cached --name-only 8bec5f7` | código só nos 3 arquivos permitidos; o resto é documentação da av3 |

## Teste que falharia sem a mudança
`caso/testes_existentes/test_reserva_estoque.py`, com `Estoque`, `GatewayFake` e `RepositorioPedidos` reais (sem `MagicMock` no estoque). Esperados vêm de R2.2. No código antigo (`01-teste-novo-falha.txt`):

```
FAIL: test_item_sem_estoque_nao_deixa_reserva
AssertionError: 8 != 10
FAIL: test_sku_repetido_falha_no_proprio_sku
AssertionError: 4 != 10
FAIL: test_sku_repetido_restaura_saldo_exato
AssertionError: 5 != 10
Ran 4 tests in 0.002s
FAILED (failures=3)
LASTEXITCODE=1
```

O caso (c) (`test_pedido_com_estoque_continua_reservando`) é guarda de regressão e passa antes e depois. A evidência 07 mostra por que o caso (b) é necessário: um desfazer via `self.reservas` passa em (a), (b2) e (c) e só (b) o pega.

## Dependências novas
Nenhuma (só biblioteca padrão; conferido em `git diff 8bec5f7..HEAD -- caso/`).

## Modo de interação e por quê
Plano primeiro (modo plano, só leitura), revisado e corrigido por mim, depois execução commit a commit com critérios de parada. Motivos: raio de impacto (duas classes, mudança pequena, mas o defeito é de estado), oráculo (R2.2 e o saldo, verificáveis por teste) e familiaridade (conheço o MiniLoja das AV1 e da AV2). Alternativa comparada: agente autônomo com edição livre, mais rápido, mas com risco concreto de desfazer via `self.reservas`, que passa na suíte existente (27 OK com o defeito presente, evidência 00, pois `test_pedidos.py` usa `MagicMock` no estoque) e erra com SKU repetido. A evidência 07 prova só que, entre os casos novos, apenas (b) pega essa armadilha.

## Limites
- R2.3 (pagamento recusado também deixa reserva): fora do escopo.
- Chave `tmp-{usuario_id}` e sobrescrita em `estoque.py:19`: pode perder a entrada de reserva de um pedido anterior do mesmo usuário e SKU; o saldo fica exato.
- `reservar` não valida `qtd <= 0`.
- Só `EstoqueInsuficiente` dispara o desfazer (ex.: item sem `sku`, evidência 08).
- O golden cobre só `calcular_total` (64 cenários da AV1.2), não o estoque.
- Execução em Windows, `python -B`, Python 3.15 (conferido com `python --version` depois da execução; não capturado nas evidências 00–07).

Mais detalhes e erros da IA: [`template-registro.md`](template-registro.md).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
