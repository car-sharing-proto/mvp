from enum import Enum


class ActiveRentResponse(str, Enum):
    ActivedCar              = 'car is already in active mode'
    SuccessfullyActivated   = 'successfully activated'