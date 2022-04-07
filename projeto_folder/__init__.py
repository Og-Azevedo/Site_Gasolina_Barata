from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = '32cf951373feaefefeb5a5fa659c9db5'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///gasolina.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Para fazer a busca por bairro você precisa estar logado!"
login_manager.login_message_category = 'alert-info'

from projeto_folder import routes


