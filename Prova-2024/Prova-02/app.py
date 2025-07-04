from flask import Flask
from flask import *

from werkzeug.security import generate_password_hash, check_password_hash
from utils.user import User

from flask_login import LoginManager
from flask_login import *


app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = 'CHAVE_SECRETA_OU_SECRET_KEY_MWAHAHAHA'

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

        # print(session)
        # print(session['users'])
        # print(session['users'][matricula])
        # print(session['users'][matricula]["email"])
        # print(session['users'][matricula]["password"])

        session.modified = True

        user = User(matricula, email, pass_hash)
        login_user(user)

        flash('Você foi cadastrado.', category='success')
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')


    