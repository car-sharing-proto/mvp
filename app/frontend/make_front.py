from app.frontend.routes import setup_routes
from flask import Flask


def make_front(app: Flask, user_service, car_service, car_mark_service, use_session_service):
    app.template_folder = './frontend/templates'
    setup_routes(app, user_service, car_service, car_mark_service, use_session_service)