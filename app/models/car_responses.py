from enum import Enum


class CarResponse(str, Enum):
    AlreadyExists           = 'car with this ID already exists'
    SuccessfullyAdded       = 'car is successfully added'
    SuccessfullyUpdated     = 'car is successfully updated'