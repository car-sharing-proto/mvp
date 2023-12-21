from app.models.car_mark_responses import CarMarkResponse


class CarMarkService():
    def __init__(self, repository):
        self.repository = repository

    def add_car_mark(self, car_mark) -> CarMarkResponse:
        if self.repository.get_car_mark(car_mark.id):
            return CarMarkResponse.AlreadyExists
        self.repository.add_car_mark(car_mark)
        return CarMarkResponse.SuccessfullyAdded

    def get_car_mark_by_id(self, id):
        return self.repository.get_car_mark(id)
    
    def get_all_car_marks(self):
        return self.repository.get_all_car_marks()
    
    def remove_car_mark_by_id(self, id) -> CarMarkResponse:
        if not self.repository.get_car_mark(id):
            return CarMarkResponse.NotFound
        self.repository.remove_car_mark(id)
        return CarMarkResponse.SuccessfullyRemoved
    
    def update_car_mark(self, car_mark) -> CarMarkResponse:
        if not self.repository.get_car_mark(car_mark.id):
            return CarMarkResponse.NotFound
        self.repository.update_car_mark(car_mark)
        return CarMarkResponse.SuccessfullyUpdated