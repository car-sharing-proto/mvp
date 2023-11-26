from app.usecases.user_register import user_register
from app.models.user import User

def user_register_controller(name, password):
    user = User(name, password, "user")
    user_register(user)