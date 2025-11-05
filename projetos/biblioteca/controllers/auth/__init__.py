from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from config import Usuario, ENGINE

auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome: str = request.form.get('nome')
        email: str = request.form.get('email')
        numero_telefone: str = request.form.get('numero_telefone')
        senha: str = request.form.get('senha')

        query = text(f"SELECT * FROM usuarios WHERE email = '{email}';")
        with ENGINE.connect() as conn:
            user_existe = conn.execute(query).fetchone()
            if user_existe:
                flash('Email já cadastrado!')
                conn.close()
                return redirect(url_for('auth.login'))

            senha_hash: str = generate_password_hash(senha)

            query_insert = text(f"""
                INSERT INTO usuarios(nome_usuario, email, numero_telefone, senha) 
                VALUES ('{nome}', '{email}', '{numero_telefone}', '{senha_hash}');
            """)

            novo_user = conn.execute(query_insert)
            conn.commit()
            user = Usuario()
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

        query = text(f"SELECT * FROM usuarios WHERE email = '{email}';")
        with ENGINE.connect() as conn:
            user_existe = conn.execute(query).fetchone()
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