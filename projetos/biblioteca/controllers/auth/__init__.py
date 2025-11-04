from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

# Se o seu root não tiver senha, tire o 1234 da parte do 'root:1234@localhost:3306'
# Se a porta do seu banco de dados for 3307, mude o 3306 para 3307.
ENGINE = create_engine('mysql+mysqldb://root:1234@localhost:3306/db_atividade17')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome: str = request.form.get('nome')
        email: str = request.form.get('email')
        numero_telefone: str = request.form.get('numero_telefone')
        senha: str = request.form.get('senha')

        query = text("SELECT * FROM usuarios WHERE email = ?;")
        with ENGINE.connect() as conn:
            user_existe = conn.execute(query, email).fetchone()
            if user_existe:
                flash('Email já cadastrado!')
                conn.close()
                return redirect(url_for('auth.login'))

            senha_hash: str = generate_password_hash(senha)

            query_insert = text("""
                INSERT INTO usuarios(nome, email, numero_telefone, senha) 
                VALUES (?, ?, ?, ?, ?);
            """)

            novo_user = conn.execute(query_insert, nome, email, numero_telefone, senha_hash)
            conn.add(novo_user)
            conn.commit()
            login_user(novo_user)
            conn.close()

            flash('Cadastro realizado', category='success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = request.form.get('email')
        senha: str = request.form.get('senha')

        query = text("SELECT * FROM usuarios WHERE email = ?;")
        with ENGINE.connect() as conn:
            user_existe = conn.execute(query, email).fetchone()
            if user_existe and check_password_hash(user_existe.senha, senha):
                login_user(user_existe)
                flash('Login feito!', category='success')
                conn.close()
                return redirect(url_for('main.index')) # Depois mudar essa rota
            else:
                flash('Email ou senha incorretos', category='error')
                conn.close()

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))