from flask_login import UserMixin
from flask import session

from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, matricula: str, email: str, password_hash: str):
        self.id = matricula
        self.matricula = matricula
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def get(cls, matricula):
        '''
        Formato do dicionário: 
        {
            user: {
                'matricula': {
                    'email': 'user@gmail.com',
                    'password': 'pass_hash'
                }
            }
        }
        '''
        
        users_list = session.get('users', {})
        # print(users_list[email])
        if matricula in users_list:
            user_data = users_list[matricula]
            return cls(
                matricula=matricula,
                email=user_data['email'],
                password_hash=user_data['password']
            )
        return None
    
    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)