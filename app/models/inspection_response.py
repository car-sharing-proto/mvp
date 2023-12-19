from enum import Enum


class InspectionResponse(str, Enum):
    AlreadyInspected        = 'car is already inspected'
    SuccessfullyStarted     = 'inspection is successfully started'