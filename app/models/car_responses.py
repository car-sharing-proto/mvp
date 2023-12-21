from enum import Enum


class CarResponse(str, Enum):
    AlreadyExists           = 'car with this ID already exists'
    NotFound                = 'car not found'
    SuccessfullyAdded       = 'car is successfully added'
    SuccessfullyUpdated     = 'car is successfully updated'
    SuccessfullyRemoved     = 'car is successfully removed'