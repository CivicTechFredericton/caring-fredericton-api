import pendulum

from core.model import BaseModel
from pynamodb.attributes import BooleanAttribute, JSONAttribute, UnicodeAttribute, NumberAttribute
from pynamodb.constants import STRING
from pynamodb.expressions.operand import Path
from services.events import constants


class RecurrenceTypeEnumUnicodeAttribute(UnicodeAttribute):
    attr_type = STRING

    def serialize(self, value):
        if value not in constants.RecurrenceType.values():
            raise ValueError(
                f"{self.attr_name} must be one of {RECURRENCE_TYPE}, not '{value}'")
        else:
            return UnicodeAttribute.serialize(self, value)


class DateAttribute(UnicodeAttribute):
    """
    This class will serializer/deserialize any date Python object and store as a unicode attribute
    """
    def serialize(self, value):
        return super(DateAttribute, self).serialize(value.strftime(constants.EVENT_DATE_FORMAT))

    def deserialize(self, value):
        return pendulum.parse(value)

    # def __ge__(self, other):
    #     return Path.__ge__(other)
    #
    # def __le__(self, other):
    #     return Path.__le__(other)


class TimeAttribute(UnicodeAttribute):
    """
    This class will serializer/deserialize any time Python object and store as a unicode attribute
    """
    def serialize(self, value):
        return super(TimeAttribute, self).serialize(value.strftime(constants.EVENT_TIME_FORMAT))

    def deserialize(self, value):
        return pendulum.parse(value)


class EventModel(BaseModel):
    class Meta:
        simple_name = 'event'
        region = BaseModel.Meta.default_region

    id = UnicodeAttribute(hash_key=True)
    owner = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    start_date = DateAttribute()
    end_date = DateAttribute()
    # full_start_date = NumberAttribute()
    start_time = TimeAttribute()
    end_time = TimeAttribute()
    # full_end_date = NumberAttribute()
    is_recurring = BooleanAttribute(default=False)
    recurrence_details = JSONAttribute(null=True)
    occurrences = JSONAttribute(default=lambda: [])
    timezone = UnicodeAttribute(default='AST')
