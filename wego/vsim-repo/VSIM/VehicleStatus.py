from enum import Enum

class VehicleStatus(Enum):
    IDLE = 'IDLE'
    EN_ROUTE = 'EN_ROUTE'
    STOPPED = 'STOPPED'
    COMPLETED = 'COMPLETED_ROUTE'