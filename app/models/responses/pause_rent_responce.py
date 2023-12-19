from enum import Enum


class PauseRentResponse(str, Enum):
    PausedCar               = 'car is already in pause mode'
    SuccessfullyPaused      = 'successfully paused'