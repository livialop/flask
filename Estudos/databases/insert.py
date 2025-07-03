import sqlite3

# insert

conn = sqlite3.connect('banco.db')

SQL = 'INSERT INTO users(nome) VALUES (?)'

nome = 'Livia'

conn.execute(SQL, (nome, ))
conn.commit()

conn.close()