from flask import Flask, render_template, request, redirect, make_response, url_for, session
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SECRET_KEY'] = "Zor{YD-}R%J?Y1=3iB*b0^]`AcYF."

chave = Fernet.generate_key()
fernet = Fernet(chave)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        pass
    
    elif request.method == 'GET':
        return render_template('cadastro.html')
    

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)