class Car():
    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.number = kwargs['number']
        self.mark_id = kwargs['mark_id']
        self.rent_state = kwargs['rent_state']
        self.rent_mode = kwargs['rent_mode']