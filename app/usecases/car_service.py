class CarService():
    def __init__(self, repository):
        self.repository = repository

    def add_car(self, car):
        self.repository.add_car(car)

    def get_car_by_id(self, id):
        return self.repository.get_car(id)
    
    def remove_car_by_id(self, id):
        return self.repository.remove_car(id)
    
    def update_car(self, car):
        self.repository.update_car(car)