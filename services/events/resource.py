from core.resource import ma
from marshmallow import fields
from services.events import constants
from webargs import ValidationError


def validate_recurrence(val):
    if not constants.RecurrenceType.has_value(val):
        raise ValidationError('Invalid value, must be one of {}'.format(constants.RecurrenceType.list_values()))


class RecurrenceDetails(ma.Schema):
    recurrence = fields.Str(required=True, missing=constants.RecurrenceType.DAILY,
                            validate=validate_recurrence)
    num_recurrences = fields.Int(missing=constants.MIN_RECURRENCE,
                                 validate=lambda val: constants.MIN_RECURRENCE <= val <= constants.MAX_RECURRENCE)
    day_of_week = fields.Int(required=False, validate=lambda val: 1 <= val <= 7)
    week_of_month = fields.Int(required=False, validate=lambda val: 1 <= val <= 4)
    day_of_month = fields.Int(required=False, validate=lambda val: 1 <= val <= 31)
    # days_of_week = fields.List(fields.Int(), validate=lambda val: 1 <= val <= 7, required=False)

    class Meta:
        strict = True


class EventSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    owner = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    start_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    start_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)
    end_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)

    class Meta:
        strict = True


class EventDetailsSchema(EventSchema):
    is_recurring = fields.Bool(missing=False)
    recurrence_details = fields.Nested(RecurrenceDetails, required=False)
    # occurrences = fields.List(fields.Str(), dump_only=True)
    timezone = fields.Str(dump_only=True)

    class Meta:
        strict = True


event_schema = EventSchema()
event_details_schema = EventDetailsSchema()

