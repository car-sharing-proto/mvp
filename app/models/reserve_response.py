from enum import Enum


class ReserveResponse(str, Enum):
    UnfinishedRent          = 'unfinished rent'
    ReservedCar             = 'car is already reserved'
    UnavailableCar          = 'car is currently unavailable'
    SuccessfullyReserved    = 'successfully reserved'