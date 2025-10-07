from sqlalchemy import Table, Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from flask_login import UserMixin
from typing import List

engine = create_engine('sqlite:///pratica102.db', echo=True)
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass

user_time = Table(
    'user_time',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('time_id', ForeignKey('time.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    senha: Mapped[str] = mapped_column(String(300))

    # Cuidado com erro aqui. A referência no backpopulates deve ser o nome exato que está atribuido na outra tabela. Ex.: times ou users
    times: Mapped[List['Time']] = relationship (
        secondary=user_time,
        back_populates='users'
    )

class Time(Base):
    __tablename__ = 'time'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(60))

    users: Mapped[List['User']] = relationship (
        secondary='user_time',
        back_populates='times'
    )