from flask import Flask, render_template
from flask import request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'RANCA TAMPA E MANDA BOI'

# lista de usuários
usuarios = {}

produtos_ = {
    'gibao' : 500,
    'bota' : 1500,
    'espora' : 200,
    'carralo' : 15000,
    'bezerro' : 3000,
    'chape' : 500,
    'oculos' : 1500,
    'capacete' : 300
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' not in session: 
        return redirect(url_for('cadastro'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if nome in usuarios.keys() and check_password_hash(usuarios[nome], senha):
            session['user'] = nome
            return redirect(url_for('produtos'))
        
        return redirect(url_for('login'))  

    return render_template('login.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        
        if nome in usuarios.keys():
            return redirect(url_for('cadastro'))
        
        senha = request.form['senha']

        senha_cripto = generate_password_hash(senha)
        usuarios[nome] = senha_cripto

        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/produtos')
def produtos():
    if 'user' in session:
        return render_template(
            'produtos.html',
            produtos=produtos_)
    return redirect(url_for('login'))


@app.route('/adicionar', methods=['POST'])
def adicionar():
    # se tem alguém logado
    prod = request.form['prod']
    valor = produtos_[prod]

    if session['user'] not in session:
        session[session['user']] = []
    
    carrinho = session.get(session['user'])
    carrinho.append(prod)
    session[session['user']] = carrinho
   
    return redirect(url_for('carrinho'))


@app.route('/carrinho')
def carrinho():
    carrinho_ = session[session.get('user')]

    soma = 0
    for x in carrinho_:
        soma = soma + produtos_[x]

    return render_template(
        'carrinho.html',
        carrinho=carrinho_, 
        valor=soma)

@app.route('/remover_do_carrinho', methods=['POST'])
def remover():
    if 'user' in session:
        session.pop('carrinho') 
    return redirect(url_for('carrinho')) 

