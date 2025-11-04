from sqlalchemy import String, Integer, ForeignKey, create_engine, Date, DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from flask_login import UserMixin
import enum

engine = create_engine('mysql+mysqldb://root:@localhost:3307/db_biblioteca', echo=True) # o Echo está sendo mantido para ver as atualizações sobre o BD
session = Session(bind=engine)

class Base(UserMixin, DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__: str = 'usuarios'
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    numero_telefone: Mapped[str] = mapped_column(String(20))
    data_inscricao: Mapped[str] = mapped_column(Date)
    multa_atual: Mapped[float] = mapped_column(DECIMAL(10,2))
    senha: Mapped[str] = mapped_column(String(200), nullable=False)

    emprestimo = relationship("Emprestimo", back_populates="usuario")

class Livro(Base):
    __tablename__: str = 'livros'
    id_livro: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(50), nullable=False)
    isbn: Mapped[str] = mapped_column(String(50), nullable=False)
    ano_publicacao: Mapped[str] = mapped_column(Date)
    qnt_disponivel: Mapped[int] = mapped_column(Integer, nullable=False)
    resumo: Mapped[str] = mapped_column(String(300))
    
    # FKs FALTA FAZER
    genero_id: Mapped[int] = mapped_column(Integer, ForeignKey('generos.id_genero'))
    editora_id: Mapped[int] = mapped_column(Integer, ForeignKey('editoras.id_editora'))
    autor_id: Mapped[int] = mapped_column(Integer, ForeignKey("autores.id_autor"))

    genero = relationship("Genero", back_populates="livro")
    editora = relationship("Editora", back_populates="livro")
    autor = relationship("Autor", back_populates="livro")
    emprestimo = relationship("Emprestimo", back_populates="livro")


class Genero(Base):
    __tablename__: str = 'generos'
    id_genero: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_genero: Mapped[str] = mapped_column(String(120), nullable=False)

    livro = relationship("Livro", back_populates="genero")

class Editora(Base):
    __tablename__: str = 'editoras'
    id_editora: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_editora: Mapped[str] = mapped_column(String(120), nullable=False)
    endereco_editora: Mapped[str] = mapped_column(String(200))

    livro = relationship("Livro", back_populates="editora") 

# Enum utilizado na tabela emprestimos
class Status(enum.Enum):
    PENDENTE = "pendente"
    DEVOLVIDO = "devolvido"
    ATRASADO = "atrasado"


class Emprestimo(Base):
    __tablename__: str = "emprestimos"
    id_emprestimo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data_emprestimo: Mapped[str] = mapped_column(Date)
    data_devolucao_prevista: Mapped[str] = mapped_column(Date)
    data_devolucao_real: Mapped[str] = mapped_column(Date)
    status_emprestimo: Mapped[Status] = mapped_column(Enum(Status))
    
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id_usuario"))
    livro_id: Mapped[int] = mapped_column(Integer, ForeignKey("livros.id_livro"))

    livro = relationship("Livro", back_populates="emprestimo")
    usuario = relationship("Usuario", back_populates="emprestimo")

class Autor(Base):
    __tablename__: str = "autores"
    id_autor: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_autor: Mapped[str] = mapped_column(String(120), nullable=False)
    nacionalidade: Mapped[str] = mapped_column(String(120))
    data_nascimento: Mapped[str] = mapped_column(Date)
    biografia: Mapped[str] = mapped_column(String(300))

    livro = relationship("Livro", back_populates="autor")