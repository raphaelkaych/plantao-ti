# Instruções para agentes

Laboratório de triagem de incidentes em Python e SQLite, parte do portfólio de Raphael Kaych. O [README](README.md) é a documentação vigente; a demo no navegador e o estudo de caso ficam no repositório [farol-de-integracoes](https://github.com/raphaelkaych/farol-de-integracoes) (`/demos/plantao-ti` e `/projetos/plantao-ti`).

## Comandos

Python 3.10 ou superior, só a biblioteca padrão.

```sh
python -m unittest -v
python plantao.py --banco demo.sqlite3 fila
```

## Regras

- Preserve a interface do CLI (`abrir`, `fila`, `resolver`, `--banco`) e os prazos por prioridade: a demo e o estudo de caso descrevem esse comportamento.
- O fechamento continua sendo uma atualização condicional, que preserva o horário da primeira resolução.
- Bancos `*.sqlite3` são locais e ficam fora do Git. Use apenas chamados fictícios.
- Mudança de comportamento exige teste em `test_plantao.py` e revisão do README e do estudo de caso no portfólio.
- Trabalhe em branch própria e abra PR para `main`.
