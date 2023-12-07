class CarRepository():
    def __init__(self):
        self.data = []
    

    def get_car(self, id):
        for car in self.data:
            if car.id == id:
                return car
            
        return None
    
    
    def add_car(self, car):
        self.data.append(car)