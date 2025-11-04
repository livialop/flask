from flask import Flask
import controllers.auth
import controllers.main
import controllers.livro
import config

app: Flask = Flask(__name__)
app.register_blueprint(controllers.auth.auth_bp)
app.register_blueprint(controllers.main.main_bp)
app.register_blueprint(controllers.livro.livros_bp)

config.config(app)

if __name__ == '__main__':
    config.start_database(app)