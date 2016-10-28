# -*- coding: utf-8 -*
class User():
    def __init__(self,id):
        self.id = id
    is_authenticated = True
    is_active = True
    is_anonymous = False
    
    def get_id(self):
        return self.id


    def set_attributes(self, fn, samaccountname, mail, givenname, sn):
        self.samaccountname = samaccountname
        self.fullname = fn
        self.mail = mail
        self.givenname = givenname
        self.sn = sn
        
    def debug(self, info):
        self.info = info

