import json

from app.models.command import Command
from app.models.central_locking_status import CentralLockingStatus
from app.models.immobilizer_status import ImmobilizerStatus
from app.models.session_state import SessionState

class CommandService():
    def __init__(self, car_service, 
                 use_session_service, telemetry_service) -> None:
        self.car_service = car_service
        self.use_session_service = use_session_service
        self.telemetry_service = telemetry_service


    def get_command_for_car(self, car_id) -> Command:
        telemetry = self.telemetry_service.\
            get_latest_telemetry_for_car(car_id)
        
        if telemetry is None:
            return Command.CloseLock
        
        data = json.loads(telemetry.data)
        
        immobilizer_status = data['immobilizer_status']
        central_locking_status = data['central_locking_status']

        session = self.use_session_service.get_last_session_by_car_id(car_id)

        if session is None or \
            session.state == SessionState.Reserved.value or \
            session.state == SessionState.Finished.value or \
            session.state == SessionState.Paused.value:
            if immobilizer_status != ImmobilizerStatus.On or \
                central_locking_status != CentralLockingStatus.On:
                return Command.CloseLock
        elif session.state == SessionState.Inspection:
            if immobilizer_status != ImmobilizerStatus.On or \
                central_locking_status != CentralLockingStatus.Off:
                return Command.OpenLock
        elif session.state == SessionState.Active:
            if immobilizer_status != ImmobilizerStatus.Off or \
                central_locking_status != CentralLockingStatus.Off:
                return Command.OpenUnlock
        
        return Command.Nothing


