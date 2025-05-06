from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

# Página Inicial
@app.route('/')
def home(): 
    return render_template('home.html')

# Página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    
    if request.method == 'POST': # Pega os dados do form
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        notificacoes = ''
        
        if request.form.get('notificacoes'):
            notificacoes = 'SIM'
        else:
            notificacoes = 'NÃO'

        response = redirect('/preferencias')

        # COOKIES
        data_expiracao = datetime.now() + timedelta(days=7)
        response.set_cookie('nome', nome, expires=data_expiracao)
        response.set_cookie('genero', genero, expires=data_expiracao)
        response.set_cookie('notificacoes', notificacoes, expires=data_expiracao)

        return response
    
    return render_template('cadastro.html')

# Página de preferências / COOKIES 
@app.route('/preferencias')
def preferencias():
    nome = request.cookies.get('nome')
    genero = request.cookies.get('genero')
    notificacoes = request.cookies.get('notificacoes')

    if not nome or not genero or notificacoes is None:
        return render_template('preferencias.html', nome=None, genero=None, notificacoes=None)

    return render_template('preferencias.html', nome=nome, genero=genero, notificacoes=notificacoes)

@app.route('/recomendar')
def recomendar():
    recomendacoes = {
        'acao': [
            'Oldboy',
            '300',
            'Dune'
        ],
        'comedia': [
            'Como perder um cara em 10 dias',
            'Juno',
            'As branquelas'
        ],
        'drama': [
            'Ainda estou aqui',
            'Brilho eterno de uma mente sem lembranças',
            'A real pain'
        ],
        'ficcao': [
            'Black Mirror: USS Callister',
            'A origem',
            'Interestelar'
        ],
        'terror': [
            'Cure',
            'Se7en',
            'Battle Royale'
        ]
    }

    genero = request.args.get('genero', '')

    if genero in recomendacoes.keys():
        filmes = recomendacoes[genero]
        return render_template('recomendar.html', genero=genero, filmes=filmes)
    
    else:
        return render_template('recomendar.html', genero=None, filmes=None)


if __name__ == '__main__':
    app.run(debug=True)