# FALTA ADICIONAR LISTA DE USUÁRIOS

from flask import Flask, render_template, url_for, session, request, redirect
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MEGADIFICIL_ME_ESCONDE'

chave = Fernet.generate_key()
fernet = Fernet(chave)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Realizar o cadastro
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        if 'users' not in session:
            session['users'] = {}
        
        if nome in session['users']:
            redirect(url_for('login'))
        else:
            senha_criptografada = criptografar(senha)
            session['users'][nome] = senha_criptografada
            session['user'] = nome 
            return redirect(url_for('dashboard'))

    return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Realizar o login
        nome = request.form.get('nome')
        senha_login = request.form.get('senha')

        if 'users' not in session:
            return redirect(url_for('register'))

        if nome in session['users']:
            senha_criptografada = session['users'][nome]
            if comparar_senhas(senha_login, senha_criptografada):
                session['user'] = nome
                return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dash')
def dashboard():
    if 'user' in session:
        nome = session['user']
        usuarios = session.get('users', {})
        return render_template('dashboard.html',
                                nome=nome, usuarios=usuarios)
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))


def criptografar(senha):
    return fernet.encrypt(senha.encode()).decode()

def comparar_senhas(senha_login, senha_criptografada):
    try:
        senha_descriptografada = fernet.decrypt(senha_criptografada.encode()).decode()
        if senha_login == senha_descriptografada:
            return True

    except:
        return False

