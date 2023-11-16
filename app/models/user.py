from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, password, role):
        self.name = name
        self.password = password
        self.role = role