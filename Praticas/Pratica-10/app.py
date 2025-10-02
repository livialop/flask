from models import User, Time
from database import session, Base, engine

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = 'ezaellyficasocantandodomeuladonaaula'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

with app.app_context():
    Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'] 

        user = User(name=name, email=email, password=password)
        session.begin()

        usuario_existente = session.query(User).where(User.email == email).first()
        if usuario_existente:
            flash('Usuário já cadastrado', category='error')
            return render_template('register.html')
        
        session.add(user)
        session.commit()
        session.close()

        return redirect(url_for('login'))

    # Se a request for GET
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(email=email, password=password)
        session.begin()
        result = session.query(User).where(User.email == email).first()
        session.close()

        if result and result.password == password:
            login_user(result)
            return redirect(url_for('times'))

        else:
            flash('Usuário ou senha incorretos', category='error')
            return redirect(url_for('login'))

    # Se a request for GET
    return render_template('login.html')

