# Registro individual — AV1.6

**Limite: uma página, incluindo evidências essenciais.** Estudante: Davi Albnes — Data: 02/11/2026
Origem: meus registros AV1.1 a AV1.3 e um contexto de time **hipotético** (fictício): 4–5 devs mantendo a MiniLoja, PRs com revisão de par e CI rodando as suítes. Meus registros são o baseline em miniatura, não a medição do time.

| Campo da medição | Meu desenho |
| --- | --- |
| Pergunta (uma frase) | Se o time adotasse um agente (Claude Code) para implementar mudanças de regra de negócio, como saberia se houve ganho real? |
| Decisão que depende da resposta | Manter, ampliar ou retirar o agente nesse tipo de tarefa ao fim do período de medição. |
| Métrica primária | Mediana do **tempo até verificado** por mudança de regra (do início da tarefa até CI verde e guardrail verde). Não uso tempo até a 1ª versão nem sugestões aceitas. |
| Guardrail de qualidade | Casos derivados de `regras.md` (esperado calculado à mão antes de ver o código) passando, e defeitos de regra escapados por semana sem aumentar. Complemento: escore de mutação nas linhas alteradas não cai abaixo do baseline. |
| Baseline (de onde vem, que período) | **Do time (real, a coletar):** 4–8 semanas de histórico de PRs de regra de negócio antes da adoção. **Miniatura (só calibra o método):** AV1.1: 1ª versão em segundos (13, 5, 25 s) contra verificado em minutos (2, 1, 1 min), logo o tempo até a 1ª versão engana. AV1.2: o golden de 64 cenários não pegou a mudança de centavos do `sum()` (624,65 virou 624,64); só a comparação própria do agente com 200 mil combinações pegou. AV1.3: escore de mutação 23/31 = 74% (medido). |
| Período e método de comparação | Antes/depois, 4–8 semanas de cada lado, mesmos tipos de mudança; mediana e intervalo, não média. Se possível, alternar tarefas comparáveis com e sem agente. |
| Confundidores previstos | Tamanho e tipo da mudança; curva de aprendizado; escopo declarado (AV1.2: revisão de 8 para 20 min, mas diff menor); sazonalidade (NATAL); mudanças no CI; revisores diferentes. |
| Como a métrica poderia ser gamificada | Encurtar "verificado" com testes tautológicos ou snapshot do próprio código (AV1.3: `test_criar_pedido` e `test_cupom_natal_com_flag` seguiram verdes sob sabotagem; `test_cenarios_gravados` só falhou pelo motivo errado); fatiar PRs; tratar uso como valor. |

**Contramedida contra a manipulação:** "verificado" exige o oráculo do contrato (`regras.md`), não só CI verde; escore de mutação nas linhas alteradas; par audita uma amostra de PRs por semana.

| Tarefa recorrente candidata | Frequência e custo atual | Verificação da saída (determinística) | Permissões mínimas e orçamento | Responsável |
| --- | --- | --- | --- | --- |
| Agente **propõe** relatório de sobreviventes de mutação por PR que toca regra | **Suposição:** ~5 PRs de regra/semana, ~30 min de revisão manual por PR (~2,5 h/semana). Na miniatura foi manual (31 mutantes). | O script calcula o escore, não o agente. Cada teste proposto: limpo OK / mutante FAILED / limpo OK. O esperado de cada teste vem de `regras.md`, nunca da saída atual do código (senão vira snapshot, como `test_cenarios_gravados` na AV1.3, que mata mutante e congela o bug). `git diff --stat` só com testes novos; sem tocar `testes/`, `regras.md` nem testes existentes. O job que lê o diff é separado do job que comenta. | Leitura do repo; escrita só em rascunho/comentário (proposta, não ação). Sem segredos; não roda em PR de fork. **Orçamento hipotético:** 10 min e teto de US$ 1 por execução. | Dono da suíte, com revisão do par |

**Limite da medição e condição para interromper ou rever:** a miniatura tem poucas execuções, uma por condição e tarefas pequenas: não mede o time. **Estimativa, não medida:** com os 2 testes novos da AV1.3, 25/31 ≈ 81%. Interromper ou rever se o guardrail piorar em 2 semanas seguidas, se o tempo cair mas mais defeitos escaparem, ou se o contrato mudar.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Sonnet 5.5; tarefa delegada e contexto: rascunhar os campos a partir dos meus registros AV1.1–AV1.3 e das minhas correções; trecho aproveitado: estrutura e redação dos campos, após revisão; minha verificação/intervenção: corrigi números e atribuições (2 tautológicos, bugs no código), defini métrica, guardrail e suposições, e conferi contra os registros. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] medição completa; [x] risco de manipulação; [x] automação com verificação; [x] limite; [ ] até uma página.
