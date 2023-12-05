from flask import Flask
from flask_login import LoginManager
from app.api.routes import setup_routes
from app.infrastructure.login import setup_loging
from app.infrastructure.test.test_user_repository import UserRepository
from app.usecases.user_service import UserService


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    user_repository = UserRepository()
    user_service = UserService(user_repository)

    setup_routes(app, user_service)
    setup_loging(app, login_manager, user_service)

    return app