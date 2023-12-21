from enum import Enum


class CentralLockingStatus(str, Enum):
    On    = 'on'
    Off   = 'off'