from enum import Enum


class RentResponse(str, Enum):
    UnfinishedRent          = 'unfinished rent'
    ReservedCar             = 'car is already reserved'
    UnavailableCar          = 'car is currently unavailable'
    ActivedRent             = 'rent is already in active mode'
    PausedRent              = 'rent is already in pause mode'
    FinishedRent            = 'rent is already finished'
    OpenDoors               = 'there are open doors'
    AlreadyInspected        = 'car is already inspected'
    SuccessfullyReserved    = 'car is successfully reserved'
    SuccessfullyStarted     = 'inspection is successfully started'
    SuccessfullyActivated   = 'rent is successfully activated'
    SuccessfullyPaused      = 'rent is successfully paused'
    SuccessfullyFinished    = 'rent is successfully finished'