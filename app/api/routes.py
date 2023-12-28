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
        telemetry_service,
        command_service):
    
      
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
        data = request.json 

        response = telemetry_service.add_telemetry(
            timedate=str(data['timedate']),
            car_id=int(data['car_id']),
            data=str(data['data']))

        if response == TelemetryResponse.AlreadyExists:
            return jsonify({
                'status': 'Error', 
                'message': response.value}), 409
        elif response == TelemetryResponse.CarNotFound:
            return jsonify({
                'status': 'Error', 
                'message': response.value}), 403
        elif response == TelemetryResponse.SuccessfullyAdded:
            return jsonify({
                'status': 'Success', 
                'message': response.value}), 201
        

    @app.route('/telemetry/get/', methods = ['GET'])
    def telemetry_get():
        car_id = int(request.args['car_id'])
        command = command_service.get_command_for_car(car_id)
        return jsonify({
                'status': 'Success', 
                'message': command.value}), 201
        