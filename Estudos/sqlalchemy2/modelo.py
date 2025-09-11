from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase
from faker import Faker

faker = Faker()

engine = create_engine('mysql://root@localhost/biblioteca')
#engine = create_engine('sqlite:///biblioteca.db')
sessao = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class Livro(Base):
    __tablename__ = 'livros'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(30))

    def __repr__(self):
        return f'Nome: {self.nome}'
    
Base.metadata.create_all(bind=engine)
    

sessao.begin()

for x in range(10):
    titulo = faker.name()
    livro = Livro(titulo=titulo)
    sessao.add(livro)

sessao.commit()
sessao.close()