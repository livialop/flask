from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, logout_user, login_required
from database import Usuario, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome: str = request.form.get('nome')
        email: str = request.form.get('email')
        numero_telefone: str = request.form.get('numero_telefone')
        data_inscricao: str = request.form.get('data_inscricao')
        senha: str = request.form.get('senha')

        user_existe: Usuario = session.query(Usuario).filter_by(email=email).first()

        if user_existe:
            flash('Email já cadastrado!')
            return redirect(url_for('auth.login'))

        senha_hash: str = generate_password_hash(senha)

        novo_user: Usuario = Usuario(nome=nome, email=email, numero_telefone=numero_telefone, data_inscricao=data_inscricao, senha=senha_hash)
        session.add(novo_user)
        session.commit()

        login_user(novo_user)
        session.close()

        flash('Cadastro realizado', category='success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = request.form.get('email')
        senha: str = request.form.get('senha')

        user_existe: Usuario = session.query(Usuario).filter_by(email=email).first()

        if user_existe and check_password_hash(user_existe.senha, senha):
            login_user(user_existe)
            flash('Login feito!', category='success')
            session.close()
            return redirect(url_for('userprofile.profile'))
        # Caso senha ou email não existam
        session.close()
        flash('Email ou senha incorretos', category='error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))