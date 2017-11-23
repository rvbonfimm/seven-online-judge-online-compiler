from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)

from application.models import tables
from application.controllers import system_controller, user_controller, exercise_controller, admin_controller, study_controller
