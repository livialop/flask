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
            INSERT INTO autores(nome_autor) VALUES ('{autor}');
            INSERT INTO editoras(nome_editora) VALUES ('{editora}');
            INSERT INTO livros(titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo) 
            VALUES ('{titulo}', (SELECT ID_autor FROM autores WHERE nome_autor = '{autor}'), '{isbn}', '{ano_publicacao}', (SELECT ID_genero FROM generos WHERE nome_genero = '{genero}'), (SELECT ID_editora FROM editoras WHERE nome_editora = '{editora}'), '{quantidade}', '{resumo}');
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
    query = text("SELECT * FROM livros;")
    with ENGINE.connect() as conn:
        livros = conn.execute(query).fetchall()
        conn.close()
    return render_template('view_livros.html', livros=livros)

@livros_bp.route('/delete_livro/<int:livro_id>', methods=['POST'])
@login_required
def delete_livro(livro_id):
    query_delete = text(f"DELETE FROM livros WHERE id = {livro_id};")
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
            UPDATE livros 
            SET titulo = '{titulo}', autor_id = (SELECT ID_autor FROM autores WHERE nome_autor = '{autor}'), isbn = '{isbn}', ano_publicacao = {ano_publicacao}, genero_id = (SELECT ID_genero FROM generos WHERE nome_genero = '{genero}'), editora_id = (SELECT ID_editora FROM editoras WHERE nome_editora = '{editora}'), quantidade_disponivel = {quantidade}, resumo = '{resumo}'
            WHERE id = {livro_id};
        """)

        with ENGINE.connect() as conn:
            conn.execute(query_update)
            conn.commit()
            conn.close()

            flash('Livro atualizado com sucesso!', category='success')
            return redirect(url_for('livros.view_livro'))
        
    return render_template('update_livro.html', livro_id=livro_id)