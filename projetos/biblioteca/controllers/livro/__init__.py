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
    if request.method == 'POST':
        titulo: str = request.form.get('titulo')
        autor: str = request.form.get('autor')
        isbn: str = request.form.get('isbn')
        ano_publicacao: int = request.form.get('ano_publicacao')
        genero: str = request.form.get('genero')
        editora: str = request.form.get('editora')
        quantidade: int = request.form.get('quantidade')
        resumo: str = request.form.get('resumo')

        query_insert = text("""
            INSERT INTO livros(titulo, autor, isbn, ano_publicacao, genero, editora, quantidade, resumo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """)

        with ENGINE.connect() as conn:
            novo_livro = conn.execute(query_insert, titulo, autor, isbn, ano_publicacao, genero, editora, quantidade, resumo)
            conn.add(novo_livro)
            conn.commit()
            conn.close()

            flash('Livro adicionado com sucesso!', category='success')
            return redirect(url_for('livros.view_livro'))
    
    return render_template('add_livro.html')

@livros_bp('/view_livros')
@login_required
def view_livro():
    query = text("SELECT * FROM livros;")
    with ENGINE.connect() as conn:
        livros = conn.execute(query).fetchall()
        conn.close()
    return render_template('view_livros.html', livros=livros)

@livros_bp.route('/delete_livro/<int:livro_id>', methods=['POST'])
@login_required
def delete_livro(livro_id):
    query_delete = text("DELETE FROM livros WHERE id = ?;")
    with ENGINE.connect() as conn:
        conn.execute(query_delete, livro_id)
        conn.commit()
        conn.close()
    
    flash('Livro deletado com sucesso!', category='success')
    return redirect(url_for('livros.view_livro'))


@livros_bp.route('/update_livro/<int:livro_id>', methods=['GET', 'POST'])
@login_required
def update_livro(livro_id):
    if request.method == 'POST':
        titulo: str = request.form.get('titulo')
        autor: str = request.form.get('autor')
        isbn: str = request.form.get('isbn')
        ano_publicacao: int = request.form.get('ano_publicacao')
        genero: str = request.form.get('genero')
        editora: str = request.form.get('editora')
        quantidade: int = request.form.get('quantidade')
        resumo: str = request.form.get('resumo')

        query_update = text("""
            UPDATE livros 
            SET titulo = ?, autor = ?, isbn = ?, ano_publicacao = ?, genero = ?, editora = ?, quantidade = ?, resumo = ?
            WHERE id = ?;
        """)

        with ENGINE.connect() as conn:
            conn.execute(query_update, titulo, autor, isbn, ano_publicacao, genero, editora, quantidade, resumo, livro_id)
            conn.commit()
            conn.close()

            flash('Livro atualizado com sucesso!', category='success')
            return redirect(url_for('livros.view_livro'))
        
    return render_template('update_livro.html', livro_id=livro_id)