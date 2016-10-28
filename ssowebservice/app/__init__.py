# -*- coding: utf-8 -*
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

from app import views
#login_manager.login_view('login') 