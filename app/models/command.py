from enum import Enum


class Command(int, Enum):
    Nothing         = 0
    CloseLock       = 1
    OpenLock        = 2
    OpenUnlock      = 3