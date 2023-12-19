import datetime

from app.models.session_state import SessionState 
from app.models.use_session import UseSession
from app.models.rent_mode import RentMode 
from app.models.role import Role 

unfinished_rent = 'unfinished rent'
reserved_car = 'car is already reserved'
unavailable_car = 'car is currently unavailable'
successfully_reserved = 'successfully reserved'

class UseSessionService():
    def __init__(self, repository, car_service, user_service) -> None:
        self.repository = repository
        self.car_service = car_service
        self.user_service = user_service

    # reserve a car
    def reserve(self, user_id, car_id) -> str:
        # check user for unfinished rent
        if not self.check_user_validity(user_id):
            return unfinished_rent
        # check car for availability
        if not self.check_car_validity(car_id):
            return reserved_car
        # get car and user models
        user = self.user_service.get_user_by_id(user_id)
        car = self.car_service.get_car_by_id(car_id)
        # check for service mode
        if user.role == Role.User and \
            car.rent_mode == RentMode.Service:
            return unavailable_car
        # create session model
        session = UseSession(
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            car_id=car_id,
            user_id=user_id,
            state=SessionState.Reserved)
        # add session into the repo
        self.repository.add_session(session)
        # return all is OK
        return successfully_reserved

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


    def get_session_by_id(self, id):
        return self.repository.get_session(id)
    

    def update_session(self, session) -> None:
        self.repository.update_session(session)


    def remove_session_by_id(self, id) -> None:
        self.repository.remove_session(id)