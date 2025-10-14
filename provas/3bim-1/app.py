from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from models import *
from database import *

# Não utilizei o models pois coloquei o UserMixin na database.py junto com a classe Base

app = Flask(__name__)
app.secret_key = 'segredo123'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))


# --------------------------------------
# As rotas começam aqui
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user_existente = session.query(User).filter_by(email=email).first()

        if user_existente:
            flash('Email já cadastrado!')
            return redirect(url_for('register'))

        novo_user = User(nome=nome, email=email, senha=senha)
        session.add(novo_user)
        session.commit()

        login_user(novo_user)

        session.close()

        flash('Usuário registrado com sucesso!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user_existente = session.query(User).filter_by(email=email).first()

        if user_existente and user_existente.senha == senha:
            login_user(user_existente)
            flash('Login realizado com sucesso!')
            session.close()
            return redirect(url_for('profile'))
        # Se a senha ou email não existir
        session.close()
        flash('Credenciais inválidas!')
    return render_template('login.html')


@app.route('/profile')
@login_required
def profile():
    # Aqui, futuramente, o aluno pode adicionar relacionamento com posts, tarefas etc.
    return render_template('profile.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Criação do banco de dados
    with app.app_context():
        Base.metadata.create_all(engine)
    app.run(debug=True)
