from flask import Flask
from database import *
from main.routes import main_bp
from auth.routes import auth_bp
from userprofile.routes import userprofile_bp
from books.routes import books_bp
import config 

app: Flask = Flask(__name__)
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(userprofile_bp)
app.register_blueprint(books_bp)

config.config(app)

if __name__ == '__main__':
# Criação do banco de dados
    config.start_database(app)