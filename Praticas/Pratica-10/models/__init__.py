from database import Base, session
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Table, Column
from typing import List


user_time = Table(
    'user_time',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('time_id', ForeignKey('time.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(120))

    times:Mapped[List['Time']] = relationship(
        secondary=user_time,
        back_populates='users'
    )

class Time(Base):
    __tablename__ = "time"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))

    estudantes:Mapped[List['User']] = relationship(
        secondary=user_time,
        back_populates='times'
    )