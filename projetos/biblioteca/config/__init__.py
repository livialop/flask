from flask import Flask
from flask_login import LoginManager
from sqlalchemy import text, create_engine

def config(app: Flask):
    app.secret_key = ')*!(&!*@%&771412JIAJD)'

    login_manager: LoginManager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        query = text("SELECT id_usuario FROM usuarios WHERE id_usuario = ?;")
        engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/db_atividade17', echo=True)
        with engine.connect() as conn:
            return conn.execute(query, user_id).fetchone()

def start_database(app: Flask):
    # Mude a porta caso necessário (normalmente fica 3306 ou 3307)
    engine = create_engine('mysql+mysqldb://root:1234@localhost:3306', echo=True) # Echo mantido para ver atualização do banco de dados
    with engine.connect() as con:
        with open("database/schema.sql") as file:
            database = text(file.read())
            con.execute(database)
    app.run(debug=True)