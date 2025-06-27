from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, session, flash

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, LoginManager
from flask_login import login_user, login_required


login_manager = LoginManager()

# Definindo o app do flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "Zor{YD-}R%J?Y1=3iB*b0^]`AcYF." # Senha gerada em um site 

login_manager.__init__(app)

class User(UserMixin):
    def __init__(self, email, senha) -> dict:
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        users_list = session['users']
        if user_id in users_list:
            data = users_list[user_id]
            user = User(email=data['email'], senha=data['senha'])
            user.id = user_id
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



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
    if 'users' not in session: # Inicializa a session com o user
        session['users'] = {}

    return render_template('index.html')

# Página de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        id = len(session['users']) + 1
        for key, data in session['users'].items():
            print(key, data)
            if email == data:
                flash('Você já possui cadastro', category='error')

                return redirect(url_for('login'))
        
        senha_cripto = generate_password_hash(senha) # Faz a criptografia da senha 

        user = User(email=email, senha=senha_cripto)
        user.id = id

        users_list = session['users']
        users_list[str(id)] = {'email':email, 'senha': senha_cripto}
        session['users'] = users_list

        print(session['users'])

        login_user(user) # Loga o usuário
        
        return redirect(url_for('login'))

    return render_template('cadastro.html')
    
# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST': # Pegando os dados do formulário para comparar o usuário que está tentando logar
        email = request.form.get('email')
        senha_login = request.form.get('senha')

        senha_cripto = session['users'][email]

        users_list = session['users']

        for id, data in users_list.items():
            if email == data and check_password_hash(senha_cripto, senha_login):
                user = User(email=email, senha=senha_cripto)
                user.id = id
                login_user(user)
                return redirect(url_for('produtos'))
        
        flash('Dados incorretos', category='error')
        redirect(url_for('login'))

    return render_template('login.html') # Se o usuário errar a senha, a página aparece novamente vazia.


# Página de Produtos
@app.route('/produtos', methods=['GET'])
@login_required
def produtos():
    return render_template('produtos.html', produtos=PRODUTOS)


@app.route('/carrinho', methods=['POST'])
@login_required
def carrinho():

    if 'carrinho' not in session: # Inicializa o carrinho na session.
        session['carrinho'] = {}

    # produtos_selecionados = {}
    for produto in request.form: # Pega os produtos selecionados por checkbox no html e adiciona na session
        if produto in PRODUTOS:
            session['carrinho'][produto] = PRODUTOS[produto]
            print(session)
            print(session['users'])

    session.modified = True # Para modificar a session, adicionando o carrinho
    return redirect(url_for('ver_carrinho'))


@app.route('/ver_carrinho', methods=['GET'])
@login_required
def ver_carrinho(): 
    # Função para visualizar os itens do carrinho, caso existam
    
    carrinho = session.get('carrinho', {})
    valor_total = sum(carrinho.values()) # Somando os valores que coloquei no dicionário PRODUTOS para ver o valor total do carrinho do usuário

    return render_template('carrinho.html', carrinho=carrinho, valor_total=valor_total)


@app.route('/remover_do_carrinho', methods=['POST'])
def remover_do_carrinho():
    if 'user' in session:
        session.pop('carrinho') # Remove os itens do carrinho, esvaziando
    return redirect(url_for('ver_carrinho')) # Retorna para ver carrinho para o usuário decidir se ele vai adicionar outros itens ou sair (logout)


# Deslogar o usuário atual
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user') # Desloga o usuário que está na session atual
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
