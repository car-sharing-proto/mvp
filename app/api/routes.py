from flask import request
from app.usecases.user_register import user_register
from app.models.user import User

def setup_routes(app):
    
    @app.route('/')
    def index():
        return 'This is the best carsharing backend!'
    
    @app.route('/cars/legacy/', methods = ['GET', 'POST', 'DELETE'])
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

