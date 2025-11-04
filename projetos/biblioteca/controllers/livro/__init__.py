from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required
from sqlalchemy import create_engine, text


livros_bp = Blueprint('livros', __name__, static_folder='static', template_folder='templates')

# Se o seu root não tiver senha, tire o 1234 da parte do 'root:1234@localhost:3306'
# Se a porta do seu banco de dados for 3307, mude o 3306 para 3307.
ENGINE = create_engine('mysql+mysqldb://root:1234@localhost:3306/db_atividade17')

@livros_bp.route('/add_livro', methods=['GET', 'POST'])
@login_required
def add_livro():
    # p o usuario adicionar livros
    pass


@livros_bp('/view_livros')
@login_required
def view_livro():
    # p o usuario visualizar os livros adicionados
    pass


@livros_bp.route('/delete_livro/<int:livro_id>', methods=['POST'])
@login_required
def delete_livro(livro_id):
    # p o usuario deletar um livro que foi adicionado
    pass


@livros_bp.route('/update_livro/<int:livro_id>', methods=['GET', 'POST'])
@login_required
def update_livro(livro_id):
    # p o usuario editar as informacoes de um livro
    pass