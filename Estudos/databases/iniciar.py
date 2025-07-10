# Código incompleto, precisa pegar o resto do example no GSA.

import sqlite3

# estabelecer uma conexao
conn = sqlite3.connect('banco.db')
conn.row_factory = sqlite3.Row

# executar instrucao de criacao de tabela(s)
with open('schema.sql') as f:
    conn.executemany(f.read()) # assim, eu posso passar tambem como argumento uma lista
    # poderia usar conn.executescript()

# fechar conexao
conn.close()