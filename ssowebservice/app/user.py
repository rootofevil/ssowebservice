# -*- coding: utf-8 -*
import datetime, jwt, logging
from config import jwt_lifetime_hours, private_key_path, jwt_algorithm
class User():
    def __init__(self,id):
        self.id = id
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.id
        
    def get_fullname(self):
        return self.fullname
        
    def get_givenname(self):
        return self.givenname
        
    def get_sn(self):
        return self.sn
        
    def get_samaccountname(self):
        return self.samaccountname
        
    def get_mail(self):
        return self.mail
        
    def get_attributes(self):
        return {'id': self.get_id(),
                'fullname': self.get_fullname(),
                'givenname': self.get_givenname(),
                'sn': self.get_sn(),
                'samaccountname': self.get_samaccountname(),
                'mail': self.get_mail()
                }

    def set_attributes(self, fn, samaccountname, mail, givenname, sn):
        self.samaccountname = samaccountname.decode('utf8')
        self.fullname = fn.decode('utf8')
        self.mail = mail.decode('utf8')
        self.givenname = givenname.decode('utf8')
        self.sn = sn.decode('utf8')
        
    def get_auth_token(self):
        now = datetime.datetime.utcnow()
        expires = now + datetime.timedelta(hours=int(jwt_lifetime_hours))
        payload = {
            'iat': now,
            'nbf': now,
            'exp': expires
        }
        payload.update(self.get_attributes())
        with open(private_key_path, 'r') as key:
            private_key = key.read()
            
        algorithm = jwt_algorithm    
        token = jwt.encode(payload, key=private_key, algorithm=algorithm)
        logging.debug(token)
        
        return {'token': token, 'expires': expires}
        
    def debug(self, info):
        self.info = info

