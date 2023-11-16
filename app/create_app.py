from flask import Flask
from app.api.routes import setup_routes

def create_app():
    app = Flask(__name__)

    setup_routes(app)

    return app