from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, role, name, password):
        super().__init__()
        self.id = id
        self.role = role
        self.name = name
        self.password = password


    def check_password(self, value):
        return self.password == value