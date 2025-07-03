from flask import Flask
from flask import *

from werkzeug.security import generate_password_hash
from utils.user import User

from flask_login import LoginManager
from flask_login import *

app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = '1$0VYhikNHL1tMgcOW$c92935453c44e19ca6c6abbdca6d91de3fabeaaa626aff89e725baf6c653467b02ef139592b3ea4e1c37b54b7286'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'users' not in session:
        session['users'] = {}
    
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in session['users']:
            flash('Email já cadastrado, volte e faça login', category='error')
            return redirect(url_for('login'))
        
        password_hash = generate_password_hash(password)

        session['users'][email] = password_hash
        session.modified = True

        user = User(email=email, password_hash=password_hash)
        login_user(user)

        flash('Você foi cadastrado!', category='success')
        return redirect(url_for('index'))
    
    return render_template('register.html')