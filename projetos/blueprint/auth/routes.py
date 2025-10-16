from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from database import *

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user_existente = session.query(User).filter_by(email=email).first()

        if user_existente:
            flash('Email já cadastrado!')
            return redirect(url_for('auth.register'))

        novo_user = User(nome=nome, email=email, senha=senha)
        session.add(novo_user)
        session.commit()

        login_user(novo_user)

        session.close()

        flash('Usuário registrado com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user_existente = session.query(User).filter_by(email=email).first()

        if user_existente and user_existente.senha == senha:
            login_user(user_existente)
            flash('Login realizado com sucesso!')
            session.close()
            return redirect(url_for('userprofile.profile'))
        # Se a senha ou email não existir
        session.close()
        flash('Credenciais inválidas!')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))