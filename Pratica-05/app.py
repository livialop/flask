from flask import Flask, render_template
from flask import request, session, redirect, url_for, flash

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user

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
        lista_usuarios = session['usuarios']
        if user_id in lista_usuarios:
            info = lista_usuarios[user_id]
            user = User(nome=info['nome'], senha=info['senha'])
            user.id = user_id
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'usuarios' not in session:
        session['usuarios'] = {}

    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        lista_usuarios = session['usuarios']

        for id, dados in lista_usuarios.items():
            if nome == dados['nome'] and senha == dados['senha']:
                user = User(nome=nome, senha=dados['senha'])
                user.id = id
                login_user(user)
                return redirect(url_for('dash'))

        flash('Dados incorretos', category='error')
        redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        id = len(session['usuarios']) + 1
        for key, info in session['usuarios'].items():
            if nome == info['nome']:

                flash('Você já possui cadastro', category='error')

                return redirect(url_for('register'))
        
        user = User(nome=nome, senha=senha)
        user.id = id
        lista_usuario = session['usuarios']
        lista_usuario[str(id)] = {'nome':nome, 'senha': senha}
        session['usuarios'] = lista_usuario
        
        print(session['usuarios'])

        login_user(user)

        return redirect(url_for('dash'))

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