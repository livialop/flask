from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

engine = create_engine("sqlite:///pratica10.db", echo=True)
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass