from enum import Enum


class DoorStatus(str, Enum):
    Open    = 'opened'
    Closed  = 'closed'