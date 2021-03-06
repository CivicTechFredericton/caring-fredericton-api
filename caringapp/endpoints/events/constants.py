from enum import Enum, unique

EVENT_DATE_FORMAT = '%Y-%m-%d'
EVENT_TIME_FORMAT = '%H:%M:%S'
MIN_RECURRENCE = 1
MAX_RECURRENCE = 10


@unique
class RecurrenceType(Enum):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    BI_WEEKLY = 'BI-WEEKLY'
    MONTHLY = 'MONTHLY'

    @classmethod
    def values(cls):
        values = [item.value for item in RecurrenceType]
        return ', '.join(values)

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class OccurrenceType(Enum):
    NEVER = 'NEVER'
    AFTER = 'AFTER'  # num occurrences
    ON = 'ON'  # after specific date

    @classmethod
    def values(cls):
        values = [item.value for item in OccurrenceType]
        return ', '.join(values)

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


@unique
class UpdateType(Enum):
    ONE_TIME = 'ONE-TIME'
    ALL = 'ALL'
    REMAINING = 'REMAINING'

    @classmethod
    def values(cls):
        values = [item.value for item in UpdateType]
        return ', '.join(values)

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
