from database import *
from flask_login import LoginManager

def config(app):
    app.secret_key = 'oii romerito senha secreta 123'

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return session.get(User, int(user_id))


def start_database(app):
    # Criação do banco de dados
    with app.app_context():
        Base.metadata.create_all(engine)
    app.run(debug=True)
