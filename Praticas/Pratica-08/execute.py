import sqlite3

conn = sqlite3.connect('banco.db')

conn.execute("PRAGMA foreign_keys = ON")
INSERT = "INSERT INTO festa(nome, valor, user_id) VALUES ('Gangnam Style 3000', 1100.2, 2), ('Eu amo minha namorada', 100000, 3), ('Oiii namorada', 99999, 4), ('Top 10 festas', 10, 6), ('Nao', 27,7)"
conn.execute(INSERT)
conn.commit()

conn.close()