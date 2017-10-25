# -*- coding: utf-8 -*
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
log_path = 'logs/error.log'
log_level = 'debug'

jwt_lifetime_hours = '8'
jwt_cookie_name = 'sso_token'
jwt_cookie_path = '/'
jwt_cookie_domain = '.gssmp.local'


zm_preauth_key = "716038ada201f18ff2d7c91a5ce9ab58ef103541b53c9085cbf5ef7643411442"
zm_preauth_url = "https://mail.03.perm.ru/service/preauth"