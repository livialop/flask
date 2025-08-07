from flask import Flask, render_template
from flask import request, session, redirect, url_for
from flask import flash

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user, current_user

from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = 'chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __init__(self, nome: str, senha: str) -> None:
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        
        return cls.query.get(user_id)

with app.app_context():
    db.create_all()


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

        user = User.query.filter_by(nome=nome).first()

        if not user:
            flash('Usuário não logado', category='error')
            return redirect(url_for('login'))

        if user.senha == senha:
            login_user(user)
            flash('Você está logado!')
            return redirect(url_for('dash'))
        
        flash('Dados incorretos', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['password']      
        resultado = User.query.filter_by(nome=nome).first()
        
        if not resultado:
            # realização do cadastro
            conexao = db.engine.connect()
            
            user = User(nome=nome, senha=senha)
            db.session.add(user)
            db.session.commit()
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