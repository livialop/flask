import sqlite3

ARQUIVO = 'schema.sql'

conn = sqlite3.connect('banco.db')

with open(ARQUIVO) as file:
    conn.executescript(file.read())

conn.close()