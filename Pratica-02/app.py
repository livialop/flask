# FALTA ADICIONAR SENHA DO USUÁRIO E CRIPTOGRAFAR A SENHA

from flask import Flask, render_template, url_for, session, request, redirect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MEGADIFICIL_ME_ESCONDE'

users = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Realizar o cadastro
        nome = request.form.get('nome')
        if nome in users:
            redirect(url_for('login'))
        else:
            users.append(nome)
            session['user'] = nome
            return redirect(url_for('dashboard'))

    return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Realizar o login
        nome = request.form.get('nome')
        if nome in users:
            session['user'] = nome
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dash')
def dashboard():
    if 'user' in session:
        nome = session['user']
        return render_template('dashboard.html', nome=nome)
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))