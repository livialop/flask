from flask_login import UserMixin
from flask import session

from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, email: str, password_hash: str):
        self.id = email
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def get(cls, email):
        '''
        Formato do dicionário: 
        {
            user: {
                'email': 'user@gmail.com',
                'password': 'pass_hash'
            }
        }
        '''
        
        users_list = session.get('users', {})
        # print(users_list[email])
        if email in users_list:
            return cls(
                email=email,
                password_hash=users_list[email]
            )
        return None
    
    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)