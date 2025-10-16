from sqlalchemy import Table, Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from flask_login import UserMixin
from typing import List

engine = create_engine('sqlite:///app.db', echo=True) 
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass

user_livro = Table(
    'user_livro',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('livro_id', ForeignKey('livros.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(200), nullable=False)

    livros: Mapped[List['Livro']] = relationship(
        secondary=user_livro,
        back_populates='users'
    )


class Livro(Base):
    __tablename__ = 'livros'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    autor: Mapped[str] = mapped_column(String(120), nullable=False)

    users: Mapped[List['User']] = relationship(
        secondary=user_livro,
        back_populates='livros'
    )