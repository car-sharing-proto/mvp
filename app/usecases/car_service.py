from app.models.car_responses import CarResponse

class CarService():
    def __init__(self, repository):
        self.repository = repository

    def add_car(self, car) -> CarResponse:
        if self.repository.get_car(car.id):
            return CarResponse.AlreadyExists
        self.repository.add_car(car)
        return CarResponse.SuccessfullyAdded

    def get_car_by_id(self, id):
        return self.repository.get_car(id)
    
    def get_all_free_cars(self):
        cars = self.repository.get_all_cars()
        result = []
        for car in cars:
            if car.is_free:
                result.append(car)
        return result
    
    def get_all_cars(self):
        return self.repository.get_all_cars()
    
    def remove_car_by_id(self, id):
        return self.repository.remove_car(id)
    
    def update_car(self, car):
        self.repository.update_car(car)
        return CarResponse.SuccessfullyUpdated