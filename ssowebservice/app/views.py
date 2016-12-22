# -*- coding: utf-8 -*
from app import app, login_manager, oauth, db
from flask import render_template, flash, redirect, jsonify, make_response, request, g
from flask_login import login_required, current_user
from user import User
from config import log_path, log_level, zm_preauth_key, zm_preauth_url
from datetime import datetime, timedelta
import logging
from time import time
import hmac, hashlib
from sqlmodel import Client, Grant, Token

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = getattr(logging, log_level.upper()), filename = log_path)



@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    user = current_user
    expires = datetime.utcnow() + timedelta(seconds=100)
    logging.debug('GrantSetter: username is ' + user.get_id())
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=user.get_id(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()



@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user=request.user)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user=request.user,
    )
    db.session.add(tok)
    db.session.commit()
    return tok

@login_manager.request_loader
def get_user_from_env(req):
    logging.info('Trying to get user from environment')
    uid = req.environ.get('REMOTE_USER')
    user = User(uid)
    logging.info(uid)
    user.set_attributes(samaccountname = req.environ.get('REMOTE_USER_SAMACCOUNTNAME'), 
                        fn = req.environ.get('REMOTE_USER_FULLNAME'),
                        givenname = req.environ.get('REMOTE_USER_GIVENNAME'),
                        sn = req.environ.get('REMOTE_USER_SN'),
                        mail = req.environ.get('REMOTE_USER_MAIL'))
    #logging.debug(req.environ.viewitems())
    return user
    

@app.route('/auth', methods = ['GET'])
@login_required
def home():
    flash(current_user.get_id())
    flash(current_user.fullname)
    flash(current_user.givenname)
    flash(current_user.sn)
    flash(current_user.mail)
    flash(current_user.samaccountname)
    logging.info(current_user.get_id())
    return render_template('base.html', user = current_user)

@app.route('/auth/get_user')
@login_required
def auth_get_user():
    return jsonify(current_user.get_attributes())

@app.route('/auth/authorize', methods = ['GET', 'POST'])
@login_required    
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = current_user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'
    
@app.route('/auth/tomail')
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

    
@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None
  
@app.route('/api/me')
@oauth.require_oauth('email')
def me():
    user = request.oauth.user
    return jsonify(email=user.email, username=user.username)
