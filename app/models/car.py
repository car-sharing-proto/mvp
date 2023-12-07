class Car():
    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.number = kwargs['number']
        self.mileage = kwargs['mileage']
        self.mark = kwargs['mark']
        self.rent_state = kwargs['rent_state']
        self.rent_mode = kwargs['rent_mode']