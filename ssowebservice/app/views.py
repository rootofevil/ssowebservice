# -*- coding: utf-8 -*
from app import app, login_manager
from flask import render_template, flash, redirect, jsonify, make_response
from flask_login import login_required, current_user
from user import User
from config import log_path, log_level, zm_preauth_key, zm_preauth_url
import logging

from time import time
import hmac, hashlib

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = getattr(logging, log_level.upper()), filename = log_path)

@login_manager.request_loader
def get_user(req):
    uid = req.environ.get('REMOTE_USER')
    user = User(uid)
    #logging.info(req.environ.get('REMOTE_USER_FULLNAME'))
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
    flash(current_user.fullname)
    flash(current_user.givenname)
    flash(current_user.sn)
    flash(current_user.mail)
    flash(current_user.samaccountname)
    logging.info(current_user.get_id())
    return render_template('base.html')

@app.route('/get_user')
@login_required
def get_user():
    return jsonify(current_user.get_attributes())
    
@app.route('/login')
def login():
    return 'login'

@app.route('/tomail')
@login_required
def tomail():
        
    timestamp = int(time()*1000)
    
    try:
        #If they're not logged in, an exception will be thrown.
        acct = current_user.mail

        pak = hmac.new(zm_preauth_key, '%s|name|0|%s'%(acct, timestamp), hashlib.sha1).hexdigest()
        response = make_response(redirect("%s?account=%s&expires=0&timestamp=%s&preauth=%s"%(zm_preauth_url, acct, timestamp, pak)))
        response.set_cookie(key = 'mail_auth', value = '1', max_age = 10)
        return response
    except:
        pass

    return redirect("/login")