from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

mensagens_usuario = {}


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')

        response = make_response(redirect(url_for('mensagens')))

        response.set_cookie('username', username)

        return response
    
    return render_template('login.html')



@app.route('/mensagens', methods=['GET', 'POST'])
def mensagens():
    username = request.cookies.get('username')

    if request.method == 'POST':
        mensagem = request.form.get('mensagem')

        if username not in mensagens_usuario:
            mensagens_usuario[username] = []

        mensagens_usuario[username].append(
            {
                'username': username,
                'texto': mensagem
            }
        )    

    mensagens = mensagens_usuario.get(username, [])
    
    return render_template('mensagens.html', username=username, mensagens=mensagens)


if __name__ == '__main__':
    app.run(debug=True)