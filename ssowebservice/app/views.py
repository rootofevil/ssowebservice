# -*- coding: utf-8 -*
from app import app, login_manager
from flask import render_template, flash, redirect
from flask_login import login_required, current_user
from user import User
from config import log_path
import logging

from time import time
import hmac, hashlib

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = log_path)

@login_manager.request_loader
def get_user(req):
    uid = req.environ.get('REMOTE_USER')
    user = User(uid)
    logging.debug(req.environ.get('REMOTE_USER_FULLNAME'))
    user.set_attributes(samaccountname = req.environ.get('REMOTE_USER_SAMACCOUNTNAME'), 
                        fn = req.environ.get('REMOTE_USER_FULLNAME'),
                        givenname = req.environ.get('REMOTE_USER_GIVENNAME'),
                        sn = req.environ.get('REMOTE_USER_SN'),
                        mail = req.environ.get('REMOTE_USER_MAIL'))
    logging.debug(req.environ.viewitems())
    return user
    

@app.route('/', methods = ['GET'])
@login_required
def home():
    flash(current_user.get_id())
    flash(current_user.fullname.decode('utf8'))
    flash(current_user.givenname.decode('utf8'))
    flash(current_user.sn.decode('utf8'))
    flash(current_user.mail.decode('utf8'))
    flash(current_user.samaccountname.decode('utf8'))
    logging.debug(current_user.fullname)
    return render_template('base.html')
    
@app.route('/login')
def login():
    return 'login'

@app.route('/tomail')
@login_required
def tomail():
    preauth_key = "716038ada201f18ff2d7c91a5ce9ab58ef103541b53c9085cbf5ef7643411442"
    preauth_url = "https://mail.03.perm.ru/service/preauth"
    
    timestamp = int(time()*1000)
    
    try:
        #If they're not logged in, an exception will be thrown.
        acct = current_user.mail

        pak = hmac.new(preauth_key, '%s|name|0|%s'%(acct, timestamp), hashlib.sha1).hexdigest()
        return redirect("%s?account=%s&expires=0&timestamp=%s&preauth=%s"%(preauth_url, acct, timestamp, pak))
    except:
        pass

    return redirect("/login")