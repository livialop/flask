from flask import Flask, render_template, request, redirect, make_response, url_for, session
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

# Definindo o app do flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "Zor{YD-}R%J?Y1=3iB*b0^]`AcYF."

# Chave para criptografia
chave = Fernet.generate_key()
fernet = Fernet(chave)

# PRODUTOS
PRODUTOS = {
    'iPhone 7':1200, 
    'Motorola X':200,
    'Samsung S24': 3000,
    'LG K10': 300,
    'Nokia Tijolo': 6000,
    'Xiaomi Redmi 8': 10,
    'LG G6': 80
}


# Página Inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if 'users' not in session:
            session['users'] = {}

        if email in session['users']:
            redirect(url_for('login')) 

        else:
            # FALTA CRIPTOGRAFAR A SENHA
            session['users'][email] = senha
            session['user'] = email

        response = make_response(
            redirect(url_for('produtos'))
        )
        data_expiracao = datetime.now() + timedelta(days=7)
        response.set_cookie('email', email, expires=data_expiracao)
        response.set_cookie('nome', nome, expires=data_expiracao)

        return response
            # COLOCAR A CRIPTOGRAFIA DE SENHA DO USUÁRIO 

    elif request.method == 'GET':
        return render_template('cadastro.html')
    
# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha_login = request.form.get('senha')

        if 'users' not in session:
            return redirect(url_for('cadastro'))
        
        if email in session['users']:
            senha = session['users'][email]
            if senha_login == senha:
                session['user'] = email
                return redirect(url_for('produtos')) 

    return render_template('login.html') # Se o usuário errar a senha, a página aparece novamente vazia.

# Deslogar o usuário atual
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))
    # FALTA ADICIONAR UMA ROTA PARA O USUÁRIO DAR LOGOUT

# Página de Produtos
@app.route('/produtos', methods=['GET'])
def produtos():
    return render_template('produtos.html', produtos=PRODUTOS)


@app.route('/carrinho', methods=['POST'])
def carrinho():
    produtos_selecionados = {}
    for produto in request.form:
        produtos_selecionados[produto] = PRODUTOS[produto]
    print(produtos_selecionados)
    return render_template('carrinho.html', produtos=produtos_selecionados)

# IDEIA DE LISTA  DE PRODUTOS -> Ser um checkbox com as opções e no final um submit para enviar as informações.
# FALTA TIRAR O HTML5 DAS PÁGINAS E USAR O FILE base.html PARA FAZER O HTML BÁSICO DAS PÁGS

# LEMBRAR DE COLOCAR OS REQUIREMENTS.TXT AO FINAL DA ATIVIDADE

if __name__ == '__main__':
    app.run(debug=True)
