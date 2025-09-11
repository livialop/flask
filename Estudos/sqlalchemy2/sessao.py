from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# pip install faker

engine = create_engine('mysql://root:@localhost/flask')

with Session(bind=engine) as sessao:
    SQL = "SELECT * FROM users"
    resultado = sessao.execute(text(SQL))
    print(type(resultado))
    print(resultado.all())