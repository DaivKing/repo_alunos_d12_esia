# Registro individual — AV1.6

**Limite: uma página, incluindo evidências essenciais.** Estudante: Davi Albnes — Data: 02/11/2026
Origem: meus registros AV1.1 a AV1.3 e um contexto de time **hipotético**: 4–5 devs mantendo a MiniLoja, PRs com revisão de par e CI rodando as suítes. Meus registros são o baseline em miniatura, não a medição do time.

| Campo da medição | Meu desenho |
| --- | --- |
| Pergunta (uma frase) | Se o time adotasse um agente para mudanças de regra de negócio, a mediana do tempo até verificado cairia sem aumentar os defeitos de regra escapados? |
| Decisão que depende da resposta | Manter, ampliar ou retirar o agente nesse tipo de tarefa ao fim do período de medição. |
| Métrica primária | Mediana do **tempo até verificado** por mudança de regra: do 1º commit da branch até o merge com CI e guardrail verdes. Não uso tempo até a 1ª versão nem sugestões aceitas. |
| Guardrail de qualidade | Casos derivados de `regras.md` (esperado calculado à mão antes de ver o código) passando, e **defeitos de regra escapados por mudança** (bug reaberto ou issue marcada "regra") sem aumentar. Complemento: escore de mutação nas linhas alteradas não cai abaixo do **baseline do time**, não dos 74% da miniatura. |
| Baseline (de onde vem, que período) | **Do time (a coletar):** 4–8 semanas de PRs de regra antes da adoção; o guardrail é reaplicado a esses PRs (se não for viável, registro a assimetria como confundidor). **Miniatura (só calibra o método):** 1ª versão em segundos contra verificado em minutos (AV1.1); o golden de 64 cenários não pegou a mudança de centavos do `sum()` (AV1.2); escore de mutação 23/31 = 74% (AV1.3). |
| Período e método de comparação | Antes/depois, 4–8 semanas de cada lado, mesmos tipos de mudança; mediana e intervalo, não média. |
| Confundidores previstos | Tamanho e tipo da mudança; curva de aprendizado; presença ou ausência de escopo declarado no PR; sazonalidade (NATAL); mudanças no CI; revisores diferentes. |
| Como a métrica poderia ser gamificada | Encurtar "verificado" com testes tautológicos ou snapshot do próprio código (AV1.3: dois testes tautológicos seguiram verdes sob sabotagem); fatiar PRs; tratar uso como valor. |

**Contramedida contra a manipulação:** "verificado" exige o oráculo do contrato (`regras.md`), não só CI verde; escore de mutação nas linhas alteradas; par audita uma amostra de PRs por semana.

| Tarefa recorrente candidata | Frequência e custo atual | Verificação da saída (determinística) | Permissões mínimas e orçamento | Responsável |
| --- | --- | --- | --- | --- |
| Agente **propõe testes para matar os sobreviventes** de mutação de cada PR que toca regra; o relatório de sobreviventes, gerado pelo script, é o insumo. | **Suposição:** ~5 PRs de regra/semana, ~30 min de revisão manual por PR (~2,5 h/semana). | O script calcula o escore, não o agente. Cada teste proposto: limpo OK / mutante FAILED / limpo OK. `git diff --stat` só com testes novos; sem tocar `testes/`, `regras.md` nem testes existentes. O job que lê o diff é separado do job que comenta. | Leitura do repo; escrita só em rascunho/comentário (proposta, não ação). Sem segredos; não roda em PR de fork. **Orçamento hipotético:** 10 min e US$ 1 por execução. | Dono da suíte; o par confere o esperado de cada teste contra `regras.md`, nunca contra a saída atual do código (senão vira snapshot, como `test_cenarios_gravados`). |

**Filtro:** frequência alta (~5 PRs/semana, suposição); verificável (o escore vem do script, não do agente); variabilidade baixa; raio de impacto baixo (só comenta, sem merge nem edição de código); custo de manter: script de mutação e prompt, revisados quando `regras.md` mudar.

**Evidência (conferível):** AV1.1, tabela T1/T2, branch `aula-1` (1ª versão 13, 5 e 25 s; verificado 2, 1 e 1 min). AV1.2, parágrafo "Limite", branch `tarefa/r2` (R$ 624,65 → 624,64). AV1.3, linha "Mutação" e tabela de sabotagens, branch `tarefa/aula-3` (31 mutantes, 23 mortos; 23 ÷ 31 = 0,742).

**Limite da medição e condição para interromper ou rever:** a miniatura tem poucas execuções, uma por condição e tarefas pequenas: não mede o time. Interromper ou rever se o guardrail piorar em 2 semanas seguidas, se o tempo cair mas mais defeitos escaparem, ou se o contrato mudar. **Desligar o agente** se tocar fora do escopo uma vez ou se mais de 30% dos testes propostos forem rejeitados em 2 semanas (30% é **suposição**).

**Procedência/IA:** minha verificação/intervenção: corrigi números e atribuições, defini métrica, guardrail e suposições, e conferi contra os registros; ferramenta e modelo visíveis: Claude Code, Sonnet 5.5 (rascunho dos campos; aproveitei estrutura e redação após revisão); apoio do Claude (chat, claude-opus-5-5) na revisão do plano e das correções. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] medição completa; [x] risco de manipulação; [x] automação com verificação; [x] limite; [x] até uma página.
