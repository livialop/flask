# Criar o ambiente

# pip install sqlalchemy
from sqlalchemy import create_engine, text

# Parte SQLITE
SQLITE = "sqlite:///database.db"
engine = create_engine(SQLITE)
# conexao = engine.connect()
with engine.connect() as conn:
    SQL = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL           
        )
    """)
    conn.execute(SQL)
    conn.commit()

# ---
# pip install mysqlclient
MYSQL = 'mysql://root:@localhost/flask'
engine = create_engine(MYSQL)
with engine.connect() as conn:
    SQL = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(120) NOT NULL           
        )
    """)
    conn.execute(SQL)
    conn.commit()

#with engine.connect() as conn:
#    SQL = "INSERT INTO users(nome) VALUES (:nome)"
#    nome = 'livia'
#    conn.execute(text(SQL), {'nome', nome})
#    conn.commit()
#    conn.close()