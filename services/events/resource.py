from core.resource import ma
from marshmallow import fields
from services.events import constants


# http://www.vertabelo.com/blog/technical-articles/again-and-again-managing-recurring-events-in-a-data-model
# https://stackoverflow.com/questions/10890480/recurring-events-schema-w-mongodb
class EventOccurenceSchema(ma.Schema):
    date = fields.Str()

    class Meta:
        strict = True


class RecurrencyDetails(ma.Schema):
    num_occurences = fields.Int(default=0)
    # day_of_week = fields.Int(required=False, validate=lambda val: 1 <= val <= 7)
    days_of_week = fields.List(fields.Str())

    class Meta:
        strict = True


class EventSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    owner = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    start_date = fields.Date(required=True, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.Date(required=True, format=constants.EVENT_DATE_FORMAT)
    start_time = fields.Time(required=True, format=constants.EVENT_TIME_FORMAT)
    end_time = fields.Time(required=True, format=constants.EVENT_TIME_FORMAT)
    timezone = fields.Str(dump_only=True)
    recurrence = fields.Str(required=True, missing=constants.OccurrenceType.ONE_TIME)
    recurrence_details = fields.Nested(RecurrencyDetails, required=False)

    class Meta:
        strict = True


class EventDetailsSchema(EventSchema):
    occurrences = fields.Nested(EventOccurenceSchema, dump_only=True)

    class Meta:
        strict = True


event_schema = EventSchema()

