from app.models.telemetry_reponses import TelemetryResponse
from app.models.telemetry import Telemetry


class TelemetryService():
    def __init__(self, repository, car_service) -> None:
        self.repository = repository
        self.car_service = car_service

    def add_telemetry(self, **kwargs) -> TelemetryResponse:
        telemetry = Telemetry(**kwargs)
        if telemetry.id and self.repository.get_telemetry(telemetry.id):
            return TelemetryResponse.AlreadyExists
        if not self.car_service.get_car_by_id(telemetry.car_id):
            return TelemetryResponse.CarNotFound
        self.repository.add_telemetry(telemetry)
        return TelemetryResponse.SuccessfullyAdded
    

    def get_telemetry_by_time_range(
            self, car_id, start_time, end_time) -> []:
        return self.repository.get_telemetry_by_time_range(
            car_id, start_time, end_time)
    

    def get_latest_telemetry_for_car(self, car_id) -> Telemetry:
        return self.repository.get_latest_telemetry_for_car(car_id)