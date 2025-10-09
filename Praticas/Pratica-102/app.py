from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
from sqlalchemy import select

# Configurações iniciais da aplicação
app = Flask(__name__)
app.secret_key = 'deus me ajude'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))


# Criando o banco de dados
with app.app_context():
    Base.metadata.create_all(engine)

# ------------------------------------------
# Rotas
@app.route('/')
def index():
    # nome = select(User.nome)
    # print(session.execute(nome).fetchall())
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user_existe = session.query(User).filter_by(email=email).first()

        if user_existe:
            flash('Usuário já está cadastrado', category='error')
            return redirect(url_for('index'))

        senha_encript = generate_password_hash(senha)
        novo_user = User(nome=nome, email=email, senha=senha_encript)
        session.add(novo_user)
        session.commit()

        login_user(novo_user)

        session.close()

        flash('Usuário cadastrado!', category='success')
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user_existe = session.query(User).filter_by(email=email).first()
        # Se o usuário existir no banco de dados
        if user_existe and check_password_hash(user_existe.senha, senha):
            login_user(user_existe)
            flash('Login realizado', category='success')
            session.close()
            return redirect(url_for('times'))
        
        session.close()
        flash('Email ou senha incorretos.', category='error')
        return redirect(url_for('login'))
    
    # Se a request for GET
    return render_template('login.html')
            
@app.route('/times')
@login_required
def times():
    user_id = current_user.id
    usuario = session.get(User, user_id)
    times = usuario.times
    session.close()
    print(current_user.times)
    return render_template('times.html', times=times)


@app.route('/add_time', methods=['GET', 'POST'])
@login_required
def add_time():
    if request.method == 'POST':
        nome = request.form['nome']

        time_existente = session.query(Time).filter_by(nome=nome).first()
        if time_existente:
            if time_existente not in current_user.times:
                current_user.times.append(time_existente)
                session.commit()
                flash('Time adicionado', category='success')
            else:
                flash('Você já adicionou esse time', category='error')

        novo_time = Time(nome=nome)
        current_user.times.append(novo_time)

        session.add(novo_time)
        session.commit()
        session.close()

        flash('Novo time criado', category='success')
        return redirect(url_for('times'))

    # Se a request for GET
    return render_template('add_time.html')

@login_required
@app.route('/remove_time/<int:time_id>', methods=['POST'])
def remove_time(time_id):
    # Busca o time pelo ID
    time = session.get(Time, time_id)

    # Se o time não existir no banco
    if not time:
        flash('Time não encontrado.', 'error')
        return redirect(url_for('times'))

    # Se o time está associado ao usuário logado
    if time in current_user.times:
        current_user.times.remove(time)  # Remove da relação
        session.commit()
        flash('Time removido da sua lista.', 'success')
    else:
        flash('Este time não está na sua lista.', 'warning')

    return redirect(url_for('times'))


@login_required
@app.route('/edit_time/<int:time_id>', methods=['GET', 'POST'])
def edit_time(time_id):
    time = session.get(Time, time_id)

    # Se o time não existir
    if not time:
        flash('Time não encontrado.', category='error')
        return redirect(url_for('times'))

    # Se o time não estiver associado ao usuário logado
    if time not in current_user.times:
        flash('Você não tem permissão para editar este time.', category='error')
        return redirect(url_for('times'))

    if request.method == 'POST':
        novo_nome = request.form.get('nome', '').strip()

        if not novo_nome:
            flash('O nome não pode ser vazio.', category='error')
            return redirect(url_for('edit_time', time_id=time_id))

        # Atualiza o nome do time
        time.nome = novo_nome
        session.commit()

        flash('Nome do time atualizado com sucesso!', category='success')
        return redirect(url_for('times'))

    # Se a request for GET
    return render_template('edit_time.html', time=time)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))