from flask import Flask
from flask_login import LoginManager
from app.api.routes import setup_routes
from app.infrastructure.login import setup_loging


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()

    setup_routes(app)
    setup_loging(app, login_manager)

    return app