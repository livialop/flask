from flask import *
from utils.func import *
import sqlite3

# Fazendo a aplicação
app = Flask(__name__)

app.secret_key = '20r0]5/reyg1@S*v*FZJ58HnH1=oAy{t<6<rx]A(QdPBq(")*Lsd"HbJgPSpVbT'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novopersonagem', methods=['GET', 'POST'])
def novopersonagem():
    if request.method == "POST":
        nome = request.form.get('nome')
        jogo_origem = request.form.get('jogo_origem')
        habilidade_principal = request.form.get('habilidade_principal')

        conn = get_connection()

        sql = "INSERT INTO personagens(nome, jogo_origem, habilidade_principal) VALUES(?, ?, ?)"

        conn.execute(sql, (nome, jogo_origem, habilidade_principal))
        conn.commit()

        close_connection()

        return redirect(url_for('personagens'))


    # Se a request for GET
    return render_template('novopersonagem.html')

@app.route('/personagens')
def personagens():

    conn = get_connection()

    sql_get_personagens = "SELECT nome, jogo_origem, habilidade_principal FROM personagens"

    personagens = conn.execute(sql_get_personagens).fetchall()
    info_personagem = {}

    for personagem in personagens:
        info_personagem[personagem[0]] = {'jogo_origem': personagem[1], 'habilidade_principal': personagem[2]}



    print(info_personagem)

    return render_template('personagens.html', nome_personagem=list(info_personagem.keys()), info_personagem=info_personagem)