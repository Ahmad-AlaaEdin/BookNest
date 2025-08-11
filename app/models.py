from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, username, password):

        self.username = username
        self.password_hash = password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username, password):
        return cls(username, generate_password_hash(password))

    def to_dict(self):
        return {"username": self.username, "password_hash": self.password_hash}

    def get_id(self):
        return self.username
