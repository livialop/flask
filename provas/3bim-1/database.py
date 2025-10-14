from sqlalchemy import Table, Column, String, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session 
from flask_login import UserMixin

engine = create_engine('sqlite:///app.db', echo=True) # Echo p ver atualização da db
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(200), nullable=False)


# As operações que tinham nesse arquivo foram implementadas diretamente no app.py com as querys do sqlalchemy