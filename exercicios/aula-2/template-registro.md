# Registro individual — AV1.2

**Limite: uma página, incluindo evidências essenciais.** Estudante: Davi Albnes — Data: 21/10/2026
Origem: `caso/miniloja/calculo.py` fictício; modalidade: execução própria.

**Golden master:** 64 entradas; gerado executando o calcular_total atual sobre 64 cenários e gravando as saídas em caso/golden_calculo.json; comparação exata por `assertEqual` em `caso/testes_existentes/test_golden_calculo.py`. Resultado: Resultado: suíte existente 27 testes OK (26 + golden) na r1 [confirme na r2]; 5 cenários anotados como divergentes de regras.md. Trocar > por >= fez o golden falhar (2 cenários na verificação do agente; 3 testes na alteração que apareceu no seu IDE).

| Medida | Rodada 1 (sem escopo) | Rodada 2 (com escopo) |
| --- | --- | --- |
| Linhas adicionadas/removidas | +28 -59 | +32 -14 |
| Arquivos alterados (e quais estavam fora do esperado) | 1 file changed (caso\miniloja\calculo.py nenhum arquivo fora do esperado, mas dentro do arquivo removeu desconto_aplicado e o bloco pass, e passou a usar constantes e dicionários não pedidos) | 1 file changed (caso\miniloja\calculo.py) |
| Mudou comportamento? (golden master) | Não | Não |
| Tempo de revisão | 8 min | 20 min |
| Idas e vindas | 5 | 4 |

**Escopo da rodada 2:** objetivo: separar desconto, frete e taxa de calcular_total em funções privadas, sem mudar nenhum resultado; pode tocar: só caso/miniloja/calculo.py; não pode tocar: assinatura pública, outros arquivos de caso/miniloja/, testes (incl. golden) e golden_calculo.json, testes/, caso/regras.md, tipo float e código aparentemente sem uso (reportar, não remover); invariantes: mesmas saídas do golden master (igualdade exata, 64 cenários), ordem desconto→frete→taxa, mesma ordem das operações em float, mesmo comportamento com a flag NATAL ligada ou desligada; pronto quando: suíte existente (com golden) verde e git diff --stat mostrando apenas calculo.py; pare e pergunte se: parecer bug ou divergência do contrato (reportar, não corrigir), precisar mudar tipo numérico ou assinatura, tocar outro arquivo ou editar/apagar teste.
**Plano do agente: o que eu cortei ou corrigi antes de executar:** Aprovei sem cortes: o plano já tinha um único arquivo, uma extração por vez com a suíte entre elas, > mantido, constantes e comentários “sem uso” preservados, a flag NATAL lida só no ramo NATAL e as duas divergências do contrato listadas como riscos para reportar, não corrigir. Isso mostra que o escopo declarado antes dirigiu o plano.
**Algo que parecia bug e eu apenas reportei:** O agente reportou o frete > 200 contra >= 200 e o arredondamento no plano e no relato final, sem corrigir. Ele não parou para perguntar porque já conhecia as divergências do golden; o plano aprovado serviu de confirmação.

**`AGENTS.md` mínimo:** 

Comandos:
- Verificações: `python -B testes/test_miniloja.py --codigo caso`
- Suíte existente (inclui golden): `python -B testes/test_miniloja.py --codigo caso --existentes`

Limites:
- Não alterar `testes/`, `caso/regras.md` nem `caso/golden_calculo.json`; 
- não editar testes para fazê-los passar. 

Convenção não óbvia:
- Refatoração preserva o comportamento atual (golden master, igualdade exata), mesmo onde diverge de `caso/regras.md`: reportar, não corrigir. Manter o laço simples no subtotal; `sum()` muda centavos.

**Trecho essencial de evidência:** --existentes: 27 testes, OK, saída 0 (golden incluído, rodado após cada extração). --codigo caso: 8 passam e 3 falham (v08, v09, v10, de cadastro), igual ao baseline. git diff --stat tarefa/golden -- caso testes: calculo.py | 46 ... 1 file changed, 32 insertions(+), 14 deletions(-). **Limite e condição para rever o escopo:** O golden master preserva o comportamento atual, inclusive os 5 desvios do contrato, e é uma amostra finita (64 cenários): na r1 o agente só detectou que sum() mudava centavos (R$ 624,65 virava 624,64) por uma comparação própria de 200 mil combinações aleatórias. O CLAUDE.md do repositório age como escopo parcial, o que pode reduzir a diferença entre as rodadas; há uma execução por rodada. Ampliar o escopo só em tarefa separada para corrigir frete e arredondamento, regerando o golden e test_cenarios_gravados; reduzir (parar) se o golden falhar ou se for preciso tocar outro arquivo.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code v2.1.306, Sonnet 5.5; tarefa delegada e contexto: criar o golden master (escopo de 2 arquivos, plano em modo plano que eu aprovei) e refatorar calcular_total nas rodadas 1 e 2; trecho aproveitado: aproveitei o JSON, o teste e a refatoração da r2; minha verificação/intervenção: rodei as duas suítes, li o diff, comparei por git diff --stat e desfiz alterações fora do escopo.; O raciocínio e a decisão registrados são meus.

**Revisão:** [x] golden master; [x] duas rodadas com números; [x] seis campos; [x] AGENTS.md; [x] até uma página.
