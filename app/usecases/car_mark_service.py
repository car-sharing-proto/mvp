class CarMarkService():
    def __init__(self, repository):
        self.repository = repository

    def add_car_mark(self, car_mark):
        self.repository.add_car_mark(car_mark)

    def get_car_mark_by_id(self, id):
        return self.repository.get_car_mark(id)
    
    def remove_car_mark_by_id(self, id):
        return self.repository.remove_car_mark(id)
    
    def update_car_mark(self, car_mark):
        self.repository.update_car_mark(car_mark)