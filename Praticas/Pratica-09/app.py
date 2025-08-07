from flask import Flask, render_template
from flask import request, session, redirect, url_for
from flask import flash

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user, current_user

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from sqlalchemy import *
import schema as schema

login_manager = LoginManager()

app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'chave_secreta'

class User(UserMixin):
    def __init__(self, nome, senha) -> None:
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        # user_id nesse caso é um nome
        with schema.users as users:
            resultado = select(users).filter_by(nome='nome')
        # conexao = engine.connect()        
            user = User(nome=resultado['nome'], senha=resultado['senha'])
            user.id = resultado['nome']
            return user


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        lista_usuarios = session['usuarios']

        for id, dados in lista_usuarios.items():
            hash = dados['senha']
            if nome == dados['nome'] and check_password_hash(hash,senha):
                user = User(nome=nome, senha=dados['senha'])
                user.id = id
                login_user(user)
                return redirect(url_for('dash'))

        flash('Dados incorretos', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']      
        resultado = select(schema.users).filter_by(nome=nome).scalar_one()
        print(resultado)
        # none
        if not resultado:
            # realização do cadastro
            sql = "INSERT INTO users(nome, senha) VALUES(?,?)"
            conexao.execute(sql, (nome, senha))
            conexao.commit()

            # definir o usuário para logar
            user = User(nome=nome, senha=senha)
            user.id = nome

            login_user(user)

            # flash('Cadastro realizado com sucesso!', category='error')
            return redirect(url_for('dash'))

        conexao.close()
        
        flash('Problema no cadastro', category='error')
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dash():
    return render_template('dash.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))