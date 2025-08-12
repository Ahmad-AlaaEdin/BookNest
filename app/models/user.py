from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, name, email, password):
        return cls(str(uuid.uuid4()), name, email, generate_password_hash(password))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
        }
