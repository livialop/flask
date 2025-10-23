from flask import Flask 
import controllers.auth
import controllers.main
import models.config

app: Flask = Flask(__name__)
app.register_blueprint(controllers.auth.auth_bp)
app.register_blueprint(controllers.main.main_bp)

models.config.config(app)

if __name__ == '__main__':
    models.config.start_database(app)