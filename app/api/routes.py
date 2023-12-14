from flask_login import current_user

from flask import request
from flask import abort

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.models.user import User
from app.models.role import Role

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
        
        if(current_user.role == Role.User):
            abort(405)

        if request.method == 'POST':
            return f"post request for {car_id}!"

        if request.method == 'DELETE':
            return f"delete request for {car_id}!"
        
    
    @app.route('/user/legacy/', methods = ['GET', 'POST', 'DELETE'])
    @login_required
    def user():
        user_id = int(request.args['user_id'])

        user = user_service.get_user_by_id(user_id)

        if request.method == 'GET':
            if user:
                return f"{user.id}, {user.name}, {user.role}, {user.password}"
            return "None"
        
        if request.method == 'POST':
            if user:
                user_name = str(request.args['user_name'])
                user_password = str(request.args['user_password'])
                user_role = user.role 
                new_user = User(user_id, user_role, user_name, user_password)
                user_service.update_user(new_user)
                return "successfully updated"
            return "user not found"


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
        id = int(request.args['id'] )       
        password = request.args['user_password']

        user = user_service.get_user_by_id(id)

        if not user:
            return "user not found"
        
        if user.password != password:
            return "incorrect password"
        
        result = login_user(user)

        app.logger.info(f"USER LOGIN IS {result}")
        
        return "successfully logined"
    
    @app.route('/auth/logout/', methods = ['POST'])
    @login_required
    def logout():
        result = logout_user()

        app.logger.info(f"USER LOGIN IS {result}")
        
        return "successfully logouted"

