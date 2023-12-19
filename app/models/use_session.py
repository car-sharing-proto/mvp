class UseSession():
    def __init__(self, id = None, **kwargs) -> None:
        self.id = id
        self.start_time = kwargs['start_time']
        self.end_time = kwargs['end_time']
        self.car_id = kwargs['car_id']
        self.user_id = kwargs['user_id']
        self.state = kwargs['state']