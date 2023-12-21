class Telemetry():
    def __init__(self, id = None, **kwargs) -> None:
        self.id = id
        self.timedate = kwargs['timedate']
        self.car_id = kwargs['car_id']
        self.left_front_door_status = kwargs['left_front_door_status']
        self.left_rear_door_status = kwargs['left_rear_door_status']
        self.right_front_door_status = kwargs['right_front_door_status']
        self.right_rear_door_status = kwargs['right_rear_door_status']
        self.trunk_status = kwargs['trunk_status']
        self.hood_status = kwargs['hood_status']
        self.geoposition = kwargs['geoposition']
        self.immobilizer_status = kwargs['immobilizer_status']
        self.central_locking_status = kwargs['central_locking_status']

        