from enum import Enum

EVENT_DATE_FORMAT = '%Y-%m-%d'
EVENT_TIME_FORMAT = '%H:%M:%S'


class OccurrenceType(Enum):
    ONE_TIME = 1
    DAILY = 2
    BI_WEEKLY = 3
    WEEKLY = 4
    MONTHLY = 5
