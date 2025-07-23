import sqlite3

# estabelecer um conexão
conexao = sqlite3.connect("banco.db")

# executar instrução de criação de 
# tabela(s)
with open('schema.sql') as f:
    conexao.executescript(f.read())

# fechar conexão
conexao.close()