from flask import Flask
from flask_login import LoginManager
from app.api.routes import setup_routes
from app.infrastructure.login import setup_loging
from app.infrastructure.db_user_repository import UserRepository
from app.infrastructure.test.test_car_repository import CarRepository
from app.usecases.user_service import UserService
from app.usecases.car_service import CarService


def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    user_repository = UserRepository()
    car_repository = CarRepository()
    user_service = UserService(user_repository)
    car_service = CarService(car_repository)

    setup_loging(app, login_manager, user_service)
    setup_routes(app, user_service)

    return app