from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("mysql+mysqldb://root:@localhost:3307/db_biblioteca_2m", echo=True) # o Echo está sendo mantido para ver as atualizações sobre o BD
session = Session(bind=engine)

result = session.execute(text("SELECT * FROM livros"))

for row in result:
    print(row)
