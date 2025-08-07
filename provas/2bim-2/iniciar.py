import sqlite3

# estabelecer um conexão
conn = sqlite3.connect("jogo.db")

# executar instrução de criação de 
# tabela(s)
with open('schema.sql') as f:
    conn.executescript(f.read())

# fechar conexão
conn.close()