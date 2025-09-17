# pip install mysqlclient
# pip install sqlalchemy
# pip install sqlalchemy_utils
from sqlalchemy import create_engine, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import create_database, database_exists
from typing import List, Optional
from datetime import datetime

DATABASE = 'mysql+mysqldb://root@localhost/busybeaver'
# busybeaver - nome
engine = create_engine(DATABASE)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(300))

    # Relationship with posts - A post can have only one user as its owner.
    posts: Mapped[List["Post"]] = relationship(back_populates="users")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
    

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Foreign Key with table users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationship with user -> One user can have as many posts as he wants.
    user: Mapped["User"] = relationship(back_populates="posts")


def create_db(engine):
    # Creating database
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            print(database_exists(engine.url))

    except Exception as e:
        print(f"Erro para criar o banco: {e}")
        return

    # Creating tables
    try: 
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

create_db(engine=engine)

# RESOLVER EM CASA -> Não estou conseguindo criar o banco de dados no workbench