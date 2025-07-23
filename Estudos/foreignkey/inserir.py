import sqlite3

conn = sqlite3.connect('banco.db')

conn.execute("PRAGMA foreign_keys = ON")
INSERT = "INSERT INTO livros(titulo, user_id) VALUES ('EU', 11)"
conn.execute(INSERT)
conn.commit()

conn.close()