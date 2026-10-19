# Registro individual — AV1.1

**Limite: uma página, incluindo evidências essenciais.** Estudante: Davi Albnes — Data: 16/10/2026
Origem: tarefas T1–T3 fictícias do enunciado; modalidade: `execução própria`.

| Tarefa | Modo | Tempo até 1ª versão | Tempo até pronto e verificado | Idas e vindas | % corrigido à mão | O que a IA errou | Como verifiquei |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A: conversar (plano), apliquei à mão | 13 s | 2 minutos até o comando mostrar só v10 falhando | 1 | menos de 1%  | Lógica do CPF correta; código colado com espaço inicial em cada linha → IndentationError. Não validou cpf ausente (R3.1) | `python -B testes/test_miniloja.py --codigo caso`: v08 e v09 ok, 8 anteriores mantidas, só v10 falha |
| T1 | B: editar com escopo (seis campos), modo manual | 5 s | 1 minuto até o comando mostrar só v10 falhando | 2 | Nada corrigido a mão | tentou ler caso/testes_existentes/ e outros módulos fora do escopo; neguei | `python -B testes/test_miniloja.py --codigo caso`: v08 e v09 ok, 8 anteriores mantidas, só v10 falha |
| T2 | B: editar com escopo (seis campos), modo manual; 3 campos + efeito em testes antigos pedem limite de escopo | 25 s | 1 min (até 11/11 verificações passando) | 1 | 0% (nada corrigido à mão) | Código do cadastro correto de primeira (valida nome, email e cpf, acumula erros, responde 422). Efeito colateral previsto: 2 testes antigos quebram (400 para cadastro sem nome; 201 para cadastro sem CPF, contra a R3.1). Não alterei esses testes. | `python -B testes/test_miniloja.py --codigo caso`: 11 ok, código 0; `--existentes`: 2 falhas por 400→422 e CPF obrigatório; `git diff`: só `cadastro.py` |

**Trecho essencial de evidência (comando e saída que sustentam "verificado"):** 

`python -B testes/test_miniloja.py --codigo caso`:

test_v08_cpf_com_digito_verificador_errado ... ok

test_v09_cpf_com_todos_os_digitos_iguais ... ok

test_v10_payload_invalido_lista_todos_os_erros ... ok

Ran 11 tests in 0.008s — OK

`python -B testes/test_miniloja.py --codigo caso --existentes`:

FAIL: test_cadastro_sem_nome_e_rejeitado (422 != 400)

FAIL: test_cadastro_valido (422 != 201)
Ran 26 tests — FAILED (failures=2)  

contrato 400→422 e cpf obrigatório (R3.4, R3.1); testes não alterados

**T3 (hipotética): raio de impacto alto**: produção às 02h, com usuários reais e pouca gente para supervisionar; um comando errado pode agravar a lentidão ou derrubar o serviço.; **oráculo disponível** parcial métricas e logs mostram se a lentidão melhorou, mas não dizem a causa; depois de uma ação, só a métrica confirma, e o dano já pode ter ocorrido.; **permissões que concederia**: somente leitura; sem escrita, sem reiniciar, sem alterar configuração; qualquer ação que mude produção exige minha aprovação explícita.; **modo e por quê:** conversar/plano (a IA propõe hipóteses e comandos, eu decido e aplico), porque o raio de impacto é alto, a reversibilidade é baixa em produção e o oráculo só confirma depois da ação. Delegaria a execução apenas para ações reversíveis e já validadas.

**Alternativa para T2:** modo A (conversar/plano; o Code propõe e eu aplico à mão). **Comparação com minha escolha (restrição e consequência):** com B (escopo + modo
manual) o Code editou em 25 s e o escopo limitou o dano (tentou ler fora da pasta na T1 e neguei). Com A eu teria de digitar mudanças em 3 campos, com risco de erro de colagem (na T1 A houve IndentationError) e mais tempo, em troca de controle total de cada linha. **Limite da comparação e condição para rever a escolha:** uma execução por modo, em tarefas pequenas e com tempos em segundos: não prova que B é melhor, só calibra meu julgamento. Reveria para A (ou plano primeiro) se o diff tocar mais de um arquivo, se a IA sair do escopo mais de uma vez ou se não houver um teste que sirva de oráculo.

**Procedência/IA:** nferramenta: Claude Code (modelo: `claude sonnet 5.5`); **tarefa delegada e contexto**: T1 e T2, sobre caso/miniloja/cadastro.py; **trecho aproveitado:** código de validação do CPF e de erros em lista; **minha verificação/intervenção:** corrigi a indentação (T1 A), neguei leitura fora do escopo, rodei o comando de verificação e conferi o diff. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] dois modos em T1; [x] evidência localizada; [x] T3 decidida; [x] alternativa e limite; [x] até uma página.