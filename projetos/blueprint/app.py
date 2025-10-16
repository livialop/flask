from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from database import *


app = Flask(__name__)
app.secret_key = 'segredo123'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))


# --------------------------------------
# Falta fazer o blueprint dessas rotas


@app.route('/profile')
@login_required
def profile():
    # Aqui, futuramente, o aluno pode adicionar relacionamento com posts, tarefas etc.
    user_id = current_user.id
    usuario = session.get(User, user_id)
    livros = usuario.livros
    session.close()
    print(current_user.livros)
    return render_template('profile.html', user=current_user, livros=livros)


@app.route('/remover_livro/<int:livro_id>', methods=['POST'])
@login_required
def remover_livro(livro_id):
    livro = session.get(Livro, livro_id)

    if not livro:
        flash('Livro não encontrado', category='error')
        return redirect(url_for('profile'))
    
    if livro in current_user.livros:
        current_user.livros.remove(livro)
        session.commit()
        flash('Livro removido com sucesso!', category='success')
    else:
        flash('Livro não encontrado', category='error')

    return redirect(url_for('profile'))

@app.route('/adicionar_livro', methods=['GET', 'POST'])
@login_required
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']

        livro = session.query(Livro).filter_by(titulo=titulo, autor=autor).first()
        if livro:
            if livro not in current_user.livros:
                current_user.livros.append(livro)
                session.commit()
                flash('Livro adicionado.', category='success')
            else:
                flash('Já adicionou esse livro.', category='error')

        novo_livro = Livro(titulo=titulo, autor=autor)
        current_user.livros.append(novo_livro)

        session.add(novo_livro)
        session.commit()
        session.close() 

        flash('Novo livro criado.', category='success')
        return redirect(url_for('profile'))
    
    return render_template('adicionar_livro.html')


if __name__ == '__main__':
    # Criação do banco de dados
    with app.app_context():
        Base.metadata.create_all(engine)
    app.run(debug=True)

