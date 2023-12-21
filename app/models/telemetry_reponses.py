from enum import Enum


class TelemetryResponse(str, Enum):
    AlreadyExists           = 'telemetry with this ID already exists'
    NotFound                = 'telemetry not found'
    CarNotFound             = 'car not found'
    SuccessfullyAdded       = 'telemetry is successfully added'
    SuccessfullyUpdated     = 'telemetry is successfully updated'
    SuccessfullyRemoved     = 'telemetry is successfully removed'