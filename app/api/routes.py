from flask_login import current_user

from flask import request
from flask import abort

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.models.car import Car
from app.models.car_mark import CarMark
from app.models.user import User
from app.models.role import Role

def setup_routes(app, user_service, car_service,
                    car_mark_service, use_session_service):
  
    
    @app.route('/cars/legacy/', methods = ['GET', 'POST', 'DELETE'])
    @login_required
    def car():
        car_id = int(request.args['car_id'])
        car = car_service.get_car_by_id(car_id)

        if request.method == 'GET':
            if car:
                return f'''
                {car.number}, {car.mark_id}, 
                {car.rent_mode}, {car.is_free}'''
            return 'car not found'
        
        if(current_user.role == Role.User):
            abort(405)

        if request.method == 'POST':
            mark_id = int(request.args['mark_id'])
            number = str(request.args['number'])
            is_free = str(request.args['is_free'])
            rent_mode = str(request.args['rent_mode'])
            new_car = Car(
                id=car_id, 
                mark_id=mark_id, 
                number=number,
                rent_mode=rent_mode,
                is_free=is_free)
            if car:
                car_service.update_car(new_car)
                return 'successfully added'
            
            car_service.add_car(new_car)
            return 'successfully updated'

        if request.method == 'DELETE':
            if car:
                car_service.remove_car_by_id(car_id)
                return "successfully deleted"
            return 'car not found'
    
    @app.route('/car_marks/legacy/', methods = ['GET', 'POST', 'DELETE'])
    @login_required
    def car_mark():
        car_mark_id = int(request.args['id'])
        car_mark = car_mark_service.get_car_mark_by_id(car_mark_id)

        if request.method == 'GET':
            if car_mark:
                return f'''
                {car_mark.model},
                {car_mark.mark}, 
                {car_mark.color}'''
            return 'car mark not found'
        
        if(current_user.role == Role.User):
            abort(405)

        if request.method == 'POST':
            model = request.args['model']
            mark = request.args['mark']
            color = request.args['color']
            new_car_mark = CarMark(
                id=car_mark_id,
                model=model,
                mark=mark,
                color=color
            )
            if car_mark:
                car_service.update_car_mark(new_car_mark)
                return 'successfully added'
            
            car_mark_service.add_car_mark(new_car_mark)
            return 'successfully updated'

        if request.method == 'DELETE':
            if car_mark:
                car_service.remove_car_mark_by_id(car_mark_id)
                return "successfully deleted"
            return 'car mark not found'
    
    @app.route('/user/legacy/', methods = ['GET', 'POST', 'DELETE'])
    @login_required
    def user():
        user_id = int(request.args['user_id'])

        user = user_service.get_user_by_id(user_id)

        if request.method == 'GET':
            if user:
                return f"{user.id}, {user.name}, {user.role}, {user.password}"
            return "user not found"
        
        if request.method == 'POST':
            if user:
                user_name = str(request.args['user_name'])
                user_password = str(request.args['user_password'])
                user_role = user.role 
                new_user = User(user_id, user_role, user_name, user_password)
                user_service.update_user(new_user)
                return "successfully updated"
            return "user not found"
        
        if request.method == 'DELETE':
            if user:
                user_service.remove_user_by_id(user_id)
                return "successfully deleted"
            return "user not found"

    @app.route('/service/reserve/', methods = ['GET'])
    @login_required
    def reserve():
        user_id = int(request.args['user_id'])
        car_id = int(request.args['car_id'])

        car = car_service.get_car_by_id(car_id)
        user = user_service.get_user_by_id(user_id)

        if not car:
            return 'car not found'
        
        if not user:
            return 'user not found'

        return use_session_service.reserve(user_id, car_id)
    
    @app.route('/service/start_inspection/', methods = ['GET'])
    @login_required
    def start_inspection():
        id = int(request.args['id'])

        session = use_session_service.get_session_by_id(id)

        if not session:
            return 'session not found'

        return use_session_service.start_inspection(id)
    
    @app.route('/service/start_active_rent/', methods = ['GET'])
    @login_required
    def start_active_rent():
        id = int(request.args['id'])

        session = use_session_service.get_session_by_id(id)

        if not session:
            return 'session not found'

        return use_session_service.start_active_rent(id)
    
    @app.route('/service/pause_active_rent/', methods = ['GET'])
    @login_required
    def pause_active_rent():
        id = int(request.args['id'])

        session = use_session_service.get_session_by_id(id)

        if not session:
            return 'session not found'

        return use_session_service.pause_active_rent(id)
    
    @app.route('/service/finish_active_rent/', methods = ['GET'])
    @login_required
    def finish_active_rent():
        id = int(request.args['id'])

        session = use_session_service.get_session_by_id(id)

        if not session:
            return 'session not found'

        return use_session_service.finish_active_rent(id)
    
    @app.route('/session/legacy/', methods = ['GET'])
    @login_required
    def session():
        id = int(request.args['id'])

        session = use_session_service.get_session_by_id(id)

        if not session:
            return 'session not found'
        
        return f'''{session.id}, {session.start_time}, {session.end_time},
                {session.car_id}, {session.user_id}, {session.state}'''

    @app.route('/auth/register/', methods = ['POST'])
    @login_required
    def register():
        if(current_user.role == Role.User):
            abort(405)
            
        name = request.args['user_name']        
        password = request.args['user_password']
        id = request.args['id']
        role = request.args['role']

        user = User(id, role, name, password)

        user_service.register_user(user)

        return "successfully registred"
