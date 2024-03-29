import datetime
import json

from app.models.door_status import DoorStatus
from app.models.rent_responses import RentResponse
from app.models.session_state import SessionState 
from app.models.use_session import UseSession
from app.models.rent_mode import RentMode 
from app.models.role import Role 

class UseSessionService():
    def __init__(self, repository, car_service, 
                 user_service, telemetry_service) -> None:
        self.repository = repository
        self.car_service = car_service
        self.user_service = user_service
        self.telemetry_service = telemetry_service

    # reserve a car
    def reserve(self, user_id, car_id) -> RentResponse:
        # check user for unfinished rent
        if not self.check_user_validity(user_id):
            return RentResponse.UnfinishedRent
        # check car for availability
        if not self.check_car_validity(car_id):
            return RentResponse.ReservedCar
        # get car and user models
        user = self.user_service.get_user_by_id(user_id)
        car = self.car_service.get_car_by_id(car_id)
        # check for service mode
        if user.role == Role.User and \
            car.rent_mode == RentMode.Service:
            return RentResponse.UnavailableCar
        # create session model
        session = UseSession(
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            car_id=car_id,
            user_id=user_id,
            state=SessionState.Reserved)
        # add session into the repo
        self.repository.add_session(session)
        # update car state
        car.is_free = False
        self.car_service.update_car(car)
        # return all is OK
        return RentResponse.SuccessfullyReserved

    # start the car inspection
    def start_inspection(self, id) -> RentResponse:
        # get the session by id
        session = self.repository.get_session(id)
        # validate the session
        if session.state == SessionState.Finished:
            return RentResponse.FinishedRent
        if session.state != SessionState.Reserved:
            return RentResponse.AlreadyInspected
        # switch state and update data
        session.state = SessionState.Inspection
        session.end_time = datetime.datetime.now()
        self.repository.update_session(session)
        # return all is OK
        return RentResponse.SuccessfullyStarted
    
    # start an active rent
    def start_active_rent(self, id) -> RentResponse:
        # get the session by id
        session = self.repository.get_session(id)
        # validate the session
        if session.state == SessionState.Finished:
            return RentResponse.FinishedRent
        if session.state != SessionState.Inspection and \
            session.state != SessionState.Paused:
            return RentResponse.ActivedRent
        # switch state and update data
        session.state = SessionState.Active
        session.end_time = datetime.datetime.now()
        self.repository.update_session(session)
        # return all is OK
        return RentResponse.SuccessfullyActivated
    
    # pause an active rent
    def pause_active_rent(self, id) -> RentResponse:
        # get the session by id
        session = self.repository.get_session(id)
        # validate the session
        if session.state == SessionState.Finished:
            return RentResponse.FinishedRent
        if session.state != SessionState.Active:
            return RentResponse.PausedRent
        if not self.check_close_ability(session.car_id):
            return RentResponse.OpenDoors
        # switch state and update data
        session.state = SessionState.Paused
        session.end_time = datetime.datetime.now()
        self.repository.update_session(session)
        # return all is OK
        return RentResponse.SuccessfullyPaused
    
    # finish an active rent
    def finish_active_rent(self, id) -> RentResponse:
        # get the session by id
        session = self.repository.get_session(id)
        # validate the session
        if session.state == SessionState.Finished:
            return RentResponse.FinishedRent
        if not self.check_close_ability(session.car_id):
            return RentResponse.OpenDoors
        # switch state and update data
        session.state = SessionState.Finished
        session.end_time = datetime.datetime.now()
        self.repository.update_session(session)
        # update car state
        car = self.car_service.get_car_by_id(session.car_id)
        car.is_free = True
        self.car_service.update_car(car)
        # return all is OK
        return RentResponse.SuccessfullyFinished

    # returns car availability
    def check_car_validity(self, id) -> bool:
        sessions = self.repository.get_sessions_by_car_id(id)
        return self.check_validity(sessions)

    # returns user rent ability
    def check_user_validity(self, id) -> bool:
        sessions = self.repository.get_sessions_by_user_id(id)
        return self.check_validity(sessions)
    
    # check model for unresolved rents 
    def check_validity(self, sessions) -> bool:
        for session in sessions:
            if session.state != SessionState.Finished:
                return False
        return True
    

    def get_user_current_session(self, user_id):
        sessions = self.repository.get_sessions_by_user_id(user_id)
        for session in sessions:
            if session.state != SessionState.Finished:
                return session
        return None
    

    def check_close_ability(self, car_id) -> bool:
        telemetry = self.telemetry_service.get_latest_telemetry_for_car(car_id)
        json_data = json.loads(telemetry.data)
        
        def find_opened_value(data):
            if isinstance(data, dict):
                for value in data.values():
                    if not find_opened_value(value):
                        return False
            elif isinstance(data, list):
                for item in data:
                    if not find_opened_value(item):
                        return False
            else:
                if data == DoorStatus.Opened.value:
                    return False
            return True
        
        return find_opened_value(json_data)
    

    def get_last_session_by_car_id(self, car_id):
        return self.repository.get_last_session_by_car_id(car_id)
    

    def get_session_by_id(self, id):
        return self.repository.get_session(id)
    

    def update_session(self, session) -> None:
        self.repository.update_session(session)


    def remove_session_by_id(self, id) -> None:
        self.repository.remove_session(id)