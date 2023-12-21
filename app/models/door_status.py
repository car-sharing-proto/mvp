from enum import Enum


class DoorStatus(str, Enum):
    Open    = 'open'
    Closed  = 'closed'