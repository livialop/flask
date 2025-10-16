from flask import Blueprint, redirect, url_for, request, flash, render_template, Response
from flask_login import login_required, current_user
from database import *

books_bp = Blueprint('books', __name__, template_folder='templates', static_folder='static')

@books_bp.route('/remover_livro/<int:livro_id>', methods=['POST'])
@login_required
def remover_livro(livro_id) -> Response:
    livro: Livro = session.get(Livro, livro_id)

    if not livro:
        flash('Livro não encontrado', category='error')
        return redirect(url_for('userprofile.profile'))
    
    if livro in current_user.livros:
        current_user.livros.remove(livro)
        session.commit()
        flash('Livro removido com sucesso!', category='success')
    else:
        flash('Livro não encontrado', category='error')

    return redirect(url_for('userprofile.profile'))


@books_bp.route('/adicionar_livro', methods=['GET', 'POST'])
@login_required
def adicionar_livro() -> Response | str:
    if request.method == 'POST':
        titulo: str = request.form['titulo']
        autor: str = request.form['autor']

        livro: Livro = session.query(Livro).filter_by(titulo=titulo, autor=autor).first()
        if livro:
            if livro not in current_user.livros:
                current_user.livros.append(livro)
                session.commit()
                flash('Livro adicionado.', category='success')
            else:
                flash('Já adicionou esse livro.', category='error')

        novo_livro: Livro = Livro(titulo=titulo, autor=autor)
        current_user.livros.append(novo_livro)

        session.add(novo_livro)
        session.commit()
        session.close() 

        flash('Novo livro criado.', category='success')
        return redirect(url_for('userprofile.profile'))
    
    return render_template('adicionar_livro.html')

