from enum import Enum


class ImmobilizerStatus(str, Enum):
    On    = 'on'
    Off   = 'off'