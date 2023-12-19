from enum import Enum

# session states
class SessionState(str, Enum):
    Reserved    = 'reserved' 
    Inspection  = 'inspection'
    Paused      = 'paused'   
    Active      = 'active'   
    Finished    = 'finished' 