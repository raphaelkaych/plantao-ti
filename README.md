# Plantão de TI

> Laboratório de triagem de incidentes pelo terminal.

**[Abra a demonstração no navegador](https://raphael-kaych.raphaelvindex.chatgpt.site/demos/plantao-ti)** para cadastrar chamados fictícios, avançar o relógio e resolver um incidente. A versão local abaixo grava o histórico em SQLite.

Um ERP fora do ar e um pedido de acesso podem chegar no mesmo minuto. Este projeto modela uma fila de suporte em que cada prioridade tem um prazo de resolução. Os chamados abertos aparecem na ordem do prazo, com indicação de atraso. A resolução fica registrada no SQLite.

| Prioridade | Cenário fictício | Prazo corrido |
| --- | --- | --- |
| P1 | ERP indisponível | 1 hora |
| P2 | Falha em uma rotina com alternativa temporária | 4 horas |
| P3 | Solicitação de acesso a relatório | 24 horas |

## Experimente

Execute na pasta do repositório, com Python 3.10 ou superior. O exemplo pressupõe um banco novo.

```text
python plantao.py abrir P3 "Acesso a relatório"
python plantao.py abrir P1 "ERP indisponível"
python plantao.py fila
python plantao.py resolver 2
python plantao.py fila --todos
python -m unittest -v
```

A primeira consulta deve mostrar o incidente `#2` antes do `#1`. Depois da resolução, `fila --todos` também mostra o histórico. O banco é criado como `plantao.sqlite3`. Use `--banco outro.sqlite3` antes do comando para separar demonstrações.

## Decisões do laboratório

- A fila prioriza a data limite. Um incidente P3 antigo pode vencer antes de um P1 recém-aberto.
- O SLA usa minutos corridos em UTC. Resolver exatamente no prazo conta como atendimento dentro do SLA.
- O fechamento é uma atualização condicional no banco, o que preserva o horário da primeira resolução se o comando for repetido.

O escopo é um único operador local. Calendários de expediente, pausas de SLA e reabertura ficam fora do modelo.
