from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import LoginManager

from app.usecases.user_register import user_register
from app.usecases.user_register import get_user
from app.usecases.user_register import get_user_by_id
from app.models.user import User

import logging

def setup_routes(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.config['SECRET_KEY'] = 'thisisasecretkey'

    @login_manager.user_loader
    def load_user(user_id):
        app.logger.info(f"USER_ID IS {int(user_id)}")
        return get_user_by_id(int(user_id))
    
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

        user = User(name, password, "user")

        user_register(user)

        return "successfully registred"
    

    @app.route('/auth/login/', methods = ['POST'])
    def login():
        name = request.args['user_name']        
        password = request.args['user_password']

        user = get_user(name)

        if not user:
            return "user not found"
        
        if user.password != password:
            return "incorrect password"
        
        login_user(user)
        
        return "successfully logined"

