from core.resource import ma
from marshmallow import fields
from services.events import constants
from webargs import ValidationError


# http://www.vertabelo.com/blog/technical-articles/again-and-again-managing-recurring-events-in-a-data-model
# https://stackoverflow.com/questions/10890480/recurring-events-schema-w-mongodb
class OccurrenceSchema(ma.Schema):
    date = fields.List(fields.Str())

    class Meta:
        strict = True


def validate_recurrence(val):
    if not constants.RecurrenceType.has_value(val):
        raise ValidationError('Invalid value, must be one of {}'.format(constants.RecurrenceType.list_values()))


class RecurrenceDetails(ma.Schema):
    recurrence = fields.Str(required=True, missing=constants.RecurrenceType.DAILY,
                            validate=validate_recurrence)
    num_recurrences = fields.Int(missing=constants.MIN_RECURRENCE,
                                 validate=lambda val: constants.MIN_RECURRENCE <= val <= constants.MAX_RECURRENCE)
    # days_of_week = fields.List(fields.Int(), validate=lambda val: 1 <= val <= 7, required=False)

    class Meta:
        strict = True


class EventSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    owner = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    is_recurring = fields.Bool(missing=False)
    recurrence_details = fields.Nested(RecurrenceDetails, required=False)
    start_date = fields.Date(required=True, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.Date(required=True, format=constants.EVENT_DATE_FORMAT)
    start_time = fields.Time(required=True, format=constants.EVENT_TIME_FORMAT)
    end_time = fields.Time(required=True, format=constants.EVENT_TIME_FORMAT)

    class Meta:
        strict = True


class EventDetailsSchema(EventSchema):
    timezone = fields.Str(dump_only=True)
    occurrences = fields.List(fields.Str, dump_only=True)

    class Meta:
        strict = True


event_schema = EventSchema()
event_details_schema = EventDetailsSchema()

