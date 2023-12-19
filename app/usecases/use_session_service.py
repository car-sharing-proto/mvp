from app.models.session_state import SessionState 
from app.models.rent_mode import RentMode 
from app.models.role import Role 

unfinished_rent = 'unfinished rent'
reserved_car = 'car is already reserved'
unavailable_car = 'car is currently unavailable'

class UseSessionService():
    def __init__(self, repository, car_service, user_service) -> None:
        self.repository = repository
        self.car_service = car_service
        self.user_service = user_service


    def reserve(self, user_id, car_id) -> str:
        if not self.check_user_validity(user_id):
            return unfinished_rent
        if not self.check_car_validity(car_id):
            return reserved_car
        
        user = self.user_service.get_user_by_id(user_id)
        car = self.car_service.get_car_by_id(car_id)

        if user.role == Role.User and \
            car.rent_mode == RentMode.Service:
            return unavailable_car

            
    def check_car_validity(self, id) -> bool:
        sessions = self.repository.get_sessions_by_car_id(id)
        return self.check_validity(sessions)


    def check_user_validity(self, id) -> bool:
        sessions = self.repository.get_sessions_by_user_id(id)
        return self.check_validity(sessions)
    

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