from flask import Flask
from flask import *

from werkzeug.security import generate_password_hash, check_password_hash
from utils.user import User

from flask_login import LoginManager
from flask_login import *


app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = 'CHAVE_SECRETA_MALIGNA_MWAHAHAHAHAHAHAAHHA'

USERS_DB = {}

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = {}

    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        email = request.form.get('email')
        password = request.form.get('password')

        str(matricula)

        if matricula in session['users']:
            flash('Aluno já cadastrado', category='error')
            return redirect(url_for('index'))

        pass_hash = generate_password_hash(password)

        session['users'][matricula] = {
            'email': email,
            'password': pass_hash
        }

        USERS_DB = {
            'matricula': matricula,
            'email': email,
            'senha': pass_hash
        }

        # print(session)
        print(session['users'])
        # print(session['users'][matricula])
        # print(session['users'][matricula]["email"])
        # print(session['users'][matricula]["password"])

        session.modified = True

        user = User(matricula, email, pass_hash)
        login_user(user)

        flash('Você foi cadastrado.', category='success')
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        if request.method == 'POST':    
            matricula = request.form.get('matricula')
            email = request.form.get('email')
            password = request.form.get('password')

            if matricula not in session['users']:
                flash('Matrícula não cadastrada', category='error')
                return redirect(url_for('index'))

            pss_hash = session['users'][matricula]['senha'] 

            user = User(matricula, email, pss_hash)

            if user.verify_password(password):
                login_user(user)        
                flash('Login realizado com sucesso!', category='success')
                return redirect(url_for('arearestrita'))
            else:
                flash('Senha incorreta.', category='error')
                return redirect(url_for('login'))

        return render_template('login.html')


@app.route('/arearestrita')
@login_required
def arearestrita():
    if 'users' not in session:
        return redirect(url_for('login'))

    email = ''
    matricula = ''
    password = ''

    for matricula_s in session['users']:
        email = session['users'][matricula_s]['email']
        password = session['users'][matricula_s]['password']
        matricula = matricula_s

    return render_template('arearestrita.html', email=email, password=password, matricula=matricula)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user() 
    session['users'] = {}
    flash('Você foi deslogado com sucesso.', 'success')
    return redirect(url_for('index'))