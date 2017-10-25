# -*- coding: utf-8 -*
from app import app, login_manager
from flask import render_template, flash, redirect, jsonify, make_response, abort, request, url_for
from flask_login import login_required, current_user
from user import User
from config import log_path, log_level, zm_preauth_key, zm_preauth_url, jwt_lifetime_hours, jwt_cookie_name, jwt_cookie_path, jwt_cookie_domains, jwt_cookie_secure
import logging

from time import time
import hmac, hashlib

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = getattr(logging, log_level.upper()), filename = log_path)

@login_manager.request_loader
def get_user(req):
    uid = req.environ.get('REMOTE_USER')
    if uid is None:
        login_manager.login_message = 'User is not authenticated by HTTPD'
        return None
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
    if request.args.get('debug'):
        flash('uid: ' + current_user.get_id())
        flash('fullname: ' + current_user.fullname)
        flash('givenname: ' + current_user.givenname)
        flash('sn: ' + current_user.sn)
        flash('mail: ' + current_user.mail)
        flash('sAMAccountname: ' + current_user.samaccountname)
        flash('token: ' + str(current_user.get_auth_token()))
    logging.info('Logon from ' + current_user.get_id())
    if current_user is not None:
        if request.args.get('url') is not None:
            redirect_url = request.args.get('url')
        else:
            redirect_url = url_for('get_user')
        response = make_response(redirect(redirect_url))
        expires = current_user.get_auth_token()['expires']
        token = current_user.get_auth_token()['token']
        for domain in jwt_cookie_domains:
            response.set_cookie(key = jwt_cookie_name, value = token, expires = expires, path = jwt_cookie_path, domain = domain, secure=jwt_cookie_secure)
        return response
    else:
        abort(403)

@app.route('/get_user')
@login_required
def get_user():
    return jsonify(current_user.get_attributes())
    

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