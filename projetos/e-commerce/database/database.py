from sqlalchemy import String, Integer, create_engine, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List
from flask_login import UserMixin

engine = create_engine('sqlite:///ecommerce.db', echo=True)
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(200), nullable=False)

    products: Mapped[List['Product']] = relationship(
        back_populates='user'
    )

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str] = mapped_column(String(250))
    preco: Mapped[float] = mapped_column(Float, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='products')