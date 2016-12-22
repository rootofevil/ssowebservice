# -*- coding: utf-8 -*
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
        self.samaccountname = self.decode_from_utf(samaccountname)
        self.fullname = self.decode_from_utf(fn)
        self.mail = self.decode_from_utf(mail)
        self.givenname = self.decode_from_utf(givenname)
        self.sn = self.decode_from_utf(sn)
        
    def decode_from_utf(self, attr):
        try:
            decoded = attr.decode('utf8')
        except AttributeError:
            decoded = attr
        return decoded
     
    def debug(self, info):
        self.info = info

