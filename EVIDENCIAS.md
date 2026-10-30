# Evidências do entregável

## Dataset público

- **Link compartilhável:** [Dataset de avaliação no LangSmith](https://smith.langchain.com/public/e3162f63-f628-4ba0-8604-cdb50cd79428/d)
- **Conteúdo verificado:** a captura mostra 15 exemplos, com colunas de entrada e saída de referência.
- **Captura:** [screenshots/dataset-15-examples.png](screenshots/dataset-15-examples.png)

## Publicação do prompt

- **Prompt:** `setup-handle/bug_to_user_story_v2`
- **Visibilidade:** publicado como público pelo script `src/push_prompts.py`.
- **Projeto de tracing no LangSmith:** <https://smith.langchain.com/projects/mba-ia-pull-evaluation-prompt>

O link do projeto pode exigir autenticação. O link compartilhável acima é o link público
do dataset; não o confundir com um link público de dashboard.

## Avaliação final

Execução em 27/10/2026, com Python 3.12.10, Ollama `gemma4:e4b` para geração e avaliação
e o dataset original de 15 exemplos.

| Métrica | Resultado | Limite |
| --- | ---: | ---: |
| Helpfulness | 0.85 | >= 0.80 |
| Correctness | 0.82 | >= 0.80 |
| F1-Score | 0.81 | >= 0.80 |
| Clarity | 0.87 | >= 0.80 |
| Precision | 0.83 | >= 0.80 |
| Média geral | 0.8374 | >= 0.80 |

- **Status:** aprovado; todas as cinco métricas e a média atingiram o limite.
- **Captura do resumo:** [screenshots/evaluation-approved-scores.png](screenshots/evaluation-approved-scores.png)
- **Log completo:** [evaluation-final.txt](evaluation-final.txt)

**Limitação observada:** no primeiro exemplo, o juiz local não retornou JSON válido em
três avaliações; o script registrou esses três scores como `0.00`. Esses zeros foram
mantidos no agregado acima. A mesma família de modelo local (`gemma4:e4b`) gerou as
respostas e atuou como juiz, portanto os resultados são específicos a essa configuração
e não constituem avaliação independente.

## Tracing de geração

As capturas abaixo mostram, em cada execução `RunnableSequence`, o relato de bug na
entrada e a User Story gerada na saída:

1. [Carrinho de compras](screenshots/trace-generation-cart.png)
2. [Orientação de tela no iOS](screenshots/trace-generation-ios.png)
3. [Imagens de produtos no Safari](screenshots/trace-generation-safari.png)

Capturas complementares:

- [Visão geral do tracing](screenshots/tracing-overview.png)
- [Trace de avaliação da clareza](screenshots/trace-evaluator-clarity.png)

Os três traces de geração atendem ao requisito de evidenciar exemplos detalhados. Há
algumas extensões inferidas pelo modelo que não estavam explícitas nos relatos
(por exemplo, comportamento adicional ao voltar para portrait ou placeholder de erro).
Considere essas telas como evidência do fluxo e dos traces, não como afirmação de que
cada detalhe gerado foi validado contra os requisitos.

## Arquivos incluídos

- `screenshots/dataset-15-examples.png`
- `screenshots/evaluation-approved-scores.png`
- `screenshots/trace-generation-cart.png`
- `screenshots/trace-generation-ios.png`
- `screenshots/trace-generation-safari.png`
- `screenshots/trace-evaluator-clarity.png`
- `screenshots/tracing-overview.png`
- `evaluation-final.txt`
