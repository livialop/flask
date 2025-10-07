from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import *

# Configurações iniciais da aplicação
app = Flask(__name__)
app.secret_key = 'deus me ajude'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))


# Criando o banco de dados
with app.app_context():
    Base.metadata.create_all(engine)

# ------------------------------------------
# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user_existe = session.query(User).filter_by(email=email).first()

        if user_existe:
            flash('Usuário já está cadastrado', category='error')
            return redirect(url_for('index'))

        senha_encript = generate_password_hash(senha)
        novo_user = User(nome=nome, email=email, senha=senha_encript)
        session.add(novo_user)
        session.commit()

        login_user(novo_user)

        session.close()

        flash('Usuário cadastrado!', category='success')
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user_existe = session.query(User).filter_by(email=email).first()
        # Se o usuário existir no banco de dados
        if user_existe and check_password_hash(user_existe.senha, senha):
            login_user(user_existe)
            flash('Login realizado', category='success')
            session.close()
            return redirect(url_for('index'))
        
        session.close()
        flash('Email ou senha incorretos.', category='error')
        return redirect(url_for('login'))
    
    # Se a request for GET
    return render_template('login.html')
            
        