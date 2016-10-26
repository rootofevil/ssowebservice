from app import app, login_manager
from flask import render_template, flash, redirect
from flask_login import login_required, current_user
from user import User

@login_manager.request_loader
def get_user(req):
    uid = req.environ.get('REMOTE_USER')
    user = User(uid)
    return user
        

@app.route('/', methods = ['GET'])
@login_required
def home():
    flash(current_user.get_id())
    return render_template('base.html')
    
@app.route('/login')
def login():
    return 'login'
