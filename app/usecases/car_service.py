class CarService():
    def __init__(self, repository):
        self.repository = repository

    def register_car(self, car):
        self.repository.add_car(car)

    def get_car_by_id(self, id):
        return self.repository.get_car(id)