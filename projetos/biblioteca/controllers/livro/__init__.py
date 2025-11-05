from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required
from sqlalchemy import text
from config import Usuario, ENGINE


livros_bp = Blueprint('livros', __name__, static_folder='static', template_folder='templates')

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

        query_insert = text(f"""
            INSERT INTO Autores(Nome_autor) VALUES ('{autor}');
            INSERT INTO Editoras(Nome_editora) VALUES ('{editora}');
            INSERT INTO Livros(Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo) 
            VALUES ('{titulo}', (SELECT ID_autor FROM Autores WHERE Nome_autor = '{autor}'), '{isbn}', '{ano_publicacao}', (SELECT ID_genero FROM Generos WHERE Nome_genero = '{genero}'), (SELECT ID_editora FROM Editoras WHERE Nome_editora = '{editora}'), '{quantidade}', '{resumo}');
        """)

        with ENGINE.connect() as conn:
            novo_livro = conn.execute(query_insert)
            conn.add(novo_livro)
            conn.commit()
            conn.close()

            flash('Livro adicionado com sucesso!', category='success')
            return redirect(url_for('livros.view_livro'))
    
    return render_template('add_livro.html')

@livros_bp.route('/view_livros')
@login_required
def view_livro():
    query = text("SELECT * FROM Livros;")
    with ENGINE.connect() as conn:
        livros = conn.execute(query).fetchall()
        conn.close()
    return render_template('view_livros.html', livros=livros)

@livros_bp.route('/delete_livro/<int:livro_id>', methods=['POST'])
@login_required
def delete_livro(livro_id):
    query_delete = text(f"DELETE FROM Livros WHERE ID_livro = {livro_id};")
    with ENGINE.connect() as conn:
        conn.execute(query_delete)
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

        query_update = text(f"""
            UPDATE Livros
            SET Titulo = '{titulo}', Autor_id = (SELECT ID_autor FROM Autores WHERE Nome_autor = '{autor}'), ISBN = '{isbn}', Ano_publicacao = {ano_publicacao}, Genero_id = (SELECT ID_genero FROM Generos WHERE Nome_genero = '{genero}'), Editora_id = (SELECT ID_editora FROM Editoras WHERE Nome_editora = '{editora}'), Quantidade_disponivel = {quantidade}, Resumo = '{resumo}'
            WHERE ID_livro = {livro_id};
        """)

        with ENGINE.connect() as conn:
            conn.execute(query_update)
            conn.commit()
            conn.close()

            flash('Livro atualizado com sucesso!', category='success')
            return redirect(url_for('livros.view_livro'))
        
    return render_template('update_livro.html', livro_id=livro_id)