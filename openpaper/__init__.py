import os
from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# Ensure that the instance folder exist.
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


# New database init
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Auth
login = LoginManager(app)
login.login_view = 'login'
# from . import auth
# app.register_blueprint(auth.bp)
# 
# from . import stream
# app.register_blueprint(stream.bp)
# 

from openpaper import routes, models