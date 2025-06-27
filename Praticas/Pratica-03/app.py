from flask import Flask, render_template, request, redirect, make_response, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Definindo o app do flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "Zor{YD-}R%J?Y1=3iB*b0^]`AcYF." # Senha gerada em um site 

# PRODUTOS -> Decidi que o site vai vender celulares. Preço ótimo
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
    nome = request.cookies.get('nome', 'Usuário') # Por default, o nome do usuário vai ser Usuário
    return render_template('index.html', nome=nome)

# Página de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if 'users' not in session: # Inicializa a session com o user
            session['users'] = {}

        if email in session['users']:
            redirect(url_for('login')) 

        
        senha_cripto = generate_password_hash(senha) # Faz a criptografia da senha 
        session['users'][email] = senha_cripto # Guarda a senha criptografada
        session['user'] = email # Faz com que a session fique assim: {pessoa@gmail.com : senha_criptografada}

        response = make_response(
            redirect(url_for('produtos'))
        )
        data_expiracao = datetime.now() + timedelta(days=7) # Para definir os sete dias dos cookies, decidi guardar o nome e email nos cookies, mas acho que apenas o nome seria necessário
        response.set_cookie('email', email, expires=data_expiracao)
        response.set_cookie('nome', nome, expires=data_expiracao)

        return response

    elif request.method == 'GET':
        return render_template('cadastro.html')
    
# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'user' not in session: # Quem não está na session não pode entrar na página de login, pois não possui o login
        return redirect(url_for('cadastro'))

    if request.method == 'POST': # Pegando os dados do formulário para comparar o usuário que está tentando logar
        email = request.form.get('email')
        senha_login = request.form.get('senha')

        senha_cripto = session['users'][email]

        if check_password_hash(senha_cripto, senha_login): # Compara a senha digitada com a senha guardada na session
                session['user'] = email
                data_expiracao = datetime.now() + timedelta(days=7) # Definindo os sete dias para os cookies expirarem
                response = make_response(redirect(url_for('produtos')))
                response.set_cookie('email', email, expires=data_expiracao)
                response.set_cookie('nome', session['users'].get('nome', 'Usuário'), expires=data_expiracao)
                return response
        else:
            return redirect(url_for('login'))

    return render_template('login.html') # Se o usuário errar a senha, a página aparece novamente vazia.


# Página de Produtos
@app.route('/produtos', methods=['GET'])
def produtos():
    return render_template('produtos.html', produtos=PRODUTOS)


@app.route('/carrinho', methods=['POST'])
def carrinho():

    if 'user' not in session: # O usuário não pode ver essa página se não estiver logado.
        return redirect(url_for('cadastro'))
    if 'carrinho' not in session: # Inicializa o carrinho na session.
        session['carrinho'] = {}

    # produtos_selecionados = {}
    for produto in request.form: # Pega os produtos selecionados por checkbox no html e adiciona na session
        if produto in PRODUTOS:
            session['carrinho'][produto] = PRODUTOS[produto]

    session.modified = True # Para modificar a session, adicionando o carrinho
    return redirect(url_for('ver_carrinho'))


@app.route('/ver_carrinho', methods=['GET'])
def ver_carrinho(): 
    # Função para visualizar os itens do carrinho, caso existam
    if 'user' not in session: # Usuário não pode entrar nessa página caso não esteja logado 
        return redirect(url_for('cadastro'))
    
    carrinho = session.get('carrinho', {})
    valor_total = sum(carrinho.values()) # Somando os valores que coloquei no dicionário PRODUTOS para ver o valor total do carrinho do usuário

    return render_template('carrinho.html', carrinho=carrinho, valor_total=valor_total)


@app.route('/remover_do_carrinho', methods=['POST'])
def remover_do_carrinho():
    if 'user' in session:
        session.pop('carrinho') # Remove os itens do carrinho, esvaziando
    return redirect(url_for('ver_carrinho')) # Retorna para ver carrinho para o usuário decidir se ele vai adicionar outros itens ou sair (logout)

# LEMBRAR DE COLOCAR OS REQUIREMENTS.TXT AO FINAL DA ATIVIDADE

# Deslogar o usuário atual
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user') # Desloga o usuário que está na session atual
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
