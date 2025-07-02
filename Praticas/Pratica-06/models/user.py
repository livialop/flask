from flask_login import UserMixin
from flask import session

class User(UserMixin):
    def __init__(self, email, senha) -> dict:
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        users_list = session['users']
        if user_id in users_list:
            data = users_list[user_id]
            user = User(email=data['email'], senha=data['senha'])
            user.id = user_id
            return user