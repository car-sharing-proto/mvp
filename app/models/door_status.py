from enum import Enum


class DoorStatus(str, Enum):
    Opened  = 'opened'
    Closed  = 'closed'