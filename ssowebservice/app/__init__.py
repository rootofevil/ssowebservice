# -*- coding: utf-8 -*
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

oauth = OAuth2Provider(app)

db = SQLAlchemy(app)

from app import views, sqlmodel
#login_manager.login_view('login') 