# import pendulum
# import datetime
from dateutil import parser

from core.model import BaseModel
from pynamodb.attributes import BooleanAttribute, ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.constants import STRING
from services.events import constants


class RecurrenceTypeEnumUnicodeAttribute(UnicodeAttribute):
    attr_type = STRING

    def serialize(self, value):
        if not constants.RecurrenceType.has_value(value):
            raise ValueError(
                f"{self.attr_name} must be one of {constants.RecurrenceType.values()}, not '{value}'")
        else:
            return UnicodeAttribute.serialize(self, value)


class RecurrenceDetails(MapAttribute):
    recurrence = RecurrenceTypeEnumUnicodeAttribute()
    num_recurrences = NumberAttribute()


class OccurrenceDetail(MapAttribute):
    occurrence_num = NumberAttribute()
    start_date = NumberAttribute()
    end_date = NumberAttribute()


class DateAttribute(UnicodeAttribute):
    """
    This class will serializer/deserialize any date Python object and store as a unicode attribute
    """
    attr_type = STRING

    def serialize(self, value):
        return super(DateAttribute, self).serialize(value.strftime(constants.EVENT_DATE_FORMAT))

    def deserialize(self, value):
        return parser.parse(value)


class TimeAttribute(UnicodeAttribute):
    """
    This class will serializer/deserialize any time Python object and store as a unicode attribute
    """
    attr_type = STRING

    def serialize(self, value):
        return super(TimeAttribute, self).serialize(value.strftime(constants.EVENT_TIME_FORMAT))

    def deserialize(self, value):
        return parser.parse(value)


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
    start_time = TimeAttribute()
    end_time = TimeAttribute()
    is_recurring = BooleanAttribute(default=False)
    recurrence_details = RecurrenceDetails(null=True, default=lambda: [])
    occurrences = ListAttribute(default=lambda: [])
    timezone = UnicodeAttribute(default='AST')
