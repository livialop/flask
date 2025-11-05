from flask import Flask
from flask_login import LoginManager, UserMixin
from sqlalchemy import text, create_engine


# Se o seu root não tiver senha, tire o 1234 da parte do 'root:1234@localhost:3306'
# Se a porta do seu banco de dados for 3307, mude o 3306 para 3307.
ENGINE = create_engine('mysql+mysqldb://root:@localhost:3307/db_atividade17')
#ENGINE = create_engine('mysql+mysqldb://root:1234@localhost:3306/db_atividade17', echo=True)

class Usuario(UserMixin):
    def __init__(self, id_usuario, email, senha) -> None:
        self.id = id_usuario
        self.email = email
        self.senha = senha
    

def config(app: Flask):
    app.secret_key = ')*!(&!*@%&771412JIAJD)'

    login_manager: LoginManager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        query = text(f"SELECT id_usuario, email, senha FROM usuarios WHERE id_usuario = {user_id};")
        with ENGINE.connect() as conn:
            result = conn.execute(query).fetchone()
            if result:
                return Usuario(result.id_usuario, result.email, result.senha)
            return None

def start_database(app: Flask):
    # Mude a porta caso necessário (normalmente fica 3306 ou 3307)
    with ENGINE.connect() as con:
        with open("database/schema.sql") as file:
            database = text(file.read())
            con.execute(database)
    app.run(debug=True)