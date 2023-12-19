from flask import Flask
from flask_login import LoginManager
from app.api.routes import setup_routes
from app.infrastructure.login import setup_loging
from app.infrastructure.db_user_repository import UserRepository
from app.infrastructure.db_car_repository import CarRepository
from app.infrastructure.db_car_mark_repository import CarMarkRepository
from app.infrastructure.db_use_session_repository import UseSessionRepository
from app.usecases.user_service import UserService
from app.usecases.car_service import CarService
from app.usecases.car_mark_service import CarMarkService
from app.usecases.use_session_service import UseSessionService
from app.frontend.make_front import make_front

from dotenv import load_dotenv


def create_app():
    load_dotenv()

    app = Flask(__name__)

    login_manager = LoginManager()
    user_repository = UserRepository()
    car_repository = CarRepository()
    car_mark_repository = CarMarkRepository()
    use_session_repository = UseSessionRepository()
    user_service = UserService(user_repository)
    car_service = CarService(car_repository)
    car_mark_service = CarMarkService(car_mark_repository)
    use_session_service = UseSessionService(use_session_repository, 
                                            car_service, user_service)

    setup_loging(app, login_manager, user_service)
    setup_routes(app, 
                 user_service, 
                 car_service, 
                 car_mark_service, 
                 use_session_service)
    
    make_front(app)

    return app