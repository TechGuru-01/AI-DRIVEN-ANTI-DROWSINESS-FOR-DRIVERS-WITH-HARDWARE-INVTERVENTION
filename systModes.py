from enum import Enum, auto

class State(Enum):
    NO_DRIVER = auto()
    AWAKE = auto()
    DROWSY = auto()
    YAWNING = auto()
    
class SystemMode(Enum):
    PRE_DRIVE = auto()
    DRIVE = auto()
    LOCKOUT = auto()

class LockoutReason:
    DROWSY_IN_AWAKE = "drowsy_in_awake"
    YAWNING = "yawning"
    DROWSY_IN_DROWSY = "drowsy_in_drowsy"