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

        query_user_existe = text("SELECT * FROM Usuarios WHERE Email = :email")
        with ENGINE.connect() as conn:
            user_existe = conn.execute(query_user_existe, {'email': email}).fetchone()
            if user_existe:
                flash('Email já cadastrado!', category='error')
                return redirect(url_for('auth.login'))

            senha_hash = generate_password_hash(senha)

            query_insert = text("""
                INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, senha)
                VALUES (:nome, :email, :numero_telefone, :senha)
            """)

            conn.execute(query_insert, {
                'nome': nome,
                'email': email,
                'numero_telefone': numero_telefone,
                'senha': senha_hash
            })
            conn.commit()

            query_user = text("SELECT * FROM Usuarios WHERE Email = :email")
            novo_user = conn.execute(query_user, {'email': email}).mappings().fetchone()

            if novo_user:

                user_obj = Usuario(
                    id_usuario=novo_user['ID_usuario'],
                    email=novo_user['Email'],
                    senha=novo_user['senha']
                )

                login_user(user_obj)

                flash('Cadastro realizado e login efetuado com sucesso!', category='success')
                return redirect(url_for('main.index'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = request.form.get('email')
        senha: str = request.form.get('senha')

        query = text("SELECT * FROM Usuarios WHERE Email = :email")
        with ENGINE.connect() as conn:
            user_existe = conn.execute(query, {'email': email}).mappings().fetchone() # mappings serve p transformar em dicionario
            print(user_existe)
            if user_existe and check_password_hash(user_existe['senha'], senha):
                user_obj = Usuario(
                    id_usuario=user_existe['ID_usuario'],
                    email=user_existe['Email'],
                    senha=user_existe['senha']
                )
                login_user(user_obj)

                flash('Login feito!', category='success')
                return redirect(url_for('main.index')) # Depois mudar essa rota
            else:
                flash('Email ou senha incorretos', category='error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))