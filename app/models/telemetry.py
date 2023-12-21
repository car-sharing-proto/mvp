class Telemetry():
    def __init__(self, id = None, **kwargs) -> None:
        self.id = id
        self.timedate = kwargs['timedate']
        self.car_id = kwargs['car_id']
        self.data = kwargs['data'].replace("'", '"')

        