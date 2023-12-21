from flask_login import current_user

from flask import jsonify, request
from flask import abort

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.models.car import Car
from app.models.car_mark import CarMark
from app.models.user import User
from app.models.role import Role

from app.models.telemetry_reponses import TelemetryResponse

def setup_routes(
        app, 
        user_service, 
        car_service,
        car_mark_service,
        use_session_service, 
        telemetry_service):


    @app.route('/car_marks/legacy/', methods = ['GET', 'POST', 'DELETE'])
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
                car_mark_service.update_car_mark(new_car_mark)
                return 'successfully added'
            
            car_mark_service.add_car_mark(new_car_mark)
            return 'successfully updated'

        if request.method == 'DELETE':
            if car_mark:
                car_mark_service.remove_car_mark_by_id(car_mark_id)
                return "successfully deleted"
            return 'car mark not found'
    
      
    @app.route('/session/legacy/', methods = ['GET'])
    @login_required
    def session():
        id = int(request.args['id'])

        session = use_session_service.get_session_by_id(id)

        if not session:
            return 'session not found'
        
        return f'''{session.id}, {session.start_time}, {session.end_time},
                {session.car_id}, {session.user_id}, {session.state}'''


    @app.route('/telemetry/send/', methods = ['POST'])
    def telemetry_send():
        telemetry_data = request.json 

        response = telemetry_service.add_telemetry(**telemetry_data)

        if response == TelemetryResponse.AlreadyExists:
            return jsonify({
                'status': 'Error', 
                'message': 'Telemetry already exists'}), 409
        elif response == TelemetryResponse.SuccessfullyAdded:
            return jsonify({
                'status': 'Success', 
                'message': 'Telemetry added successfully'}), 201