from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.usecases.user_register import user_register
from app.usecases.user_register import get_user
from app.usecases.user_register import get_user_by_id
from app.models.user import User

import logging

def setup_routes(app, user_service):
    @app.route('/')
    def index():
        return 'This is the best carsharing backend!'
    
    
    @app.route('/cars/legacy/', methods = ['GET', 'POST', 'DELETE'])
    @login_required
    def car():
        car_id = request.args['car_id']

        if request.method == 'GET':
            return car_id

        if request.method == 'POST':
            return f"post request for {car_id}!"

        if request.method == 'DELETE':
            return f"delete request for {car_id}!"
        

    @app.route('/auth/register/', methods = ['POST'])
    def register():
        name = request.args['user_name']        
        password = request.args['user_password']
        id = request.args['id']

        user = User(id, "user", name, password)

        user_service.register_user(user)

        return "successfully registred"
    

    @app.route('/auth/login/', methods = ['POST'])
    def login():
        id = request.args['id']        
        password = request.args['user_password']

        user = user_service.get_user_by_id(id)

        if not user:
            return "user not found"
        
        if user.password != password:
            return "incorrect password"
        
        result = login_user(user)

        app.logger.info(f"USER LOGIN IS {result}")
        
        return "successfully logined"

