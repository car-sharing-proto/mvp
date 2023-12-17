from flask import Flask
from flask_login import LoginManager
from app.api.routes import setup_routes
from app.infrastructure.login import setup_loging
from app.infrastructure.db_user_repository import UserRepository
from app.infrastructure.db_car_repository import CarRepository
from app.infrastructure.db_car_mark_repository import CarMarkRepository
from app.usecases.user_service import UserService
from app.usecases.car_service import CarService
from app.usecases.car_mark_service import CarMarkService

from dotenv import load_dotenv


def create_app():
    load_dotenv()

    app = Flask(__name__)

    login_manager = LoginManager()
    user_repository = UserRepository()
    car_repository = CarRepository()
    car_mark_repository = CarMarkRepository()
    user_service = UserService(user_repository)
    car_service = CarService(car_repository)
    car_mark_service = CarMarkService(car_mark_repository)

    setup_loging(app, login_manager, user_service)
    setup_routes(app, user_service, car_service, car_mark_service)

    return app