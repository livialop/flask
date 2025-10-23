from sqlalchemy import insert
from database.database import session, Product, User
# Fazer os inserts de produtos aqui
# 1 insert deu certo. Pedir ao chat para fazer inserts depois

produto1 = Product(id=1, nome='rato', descricao='rato feio e pequeno', preco=27.5, user_id=1)

session.add(produto1)
session.commit()