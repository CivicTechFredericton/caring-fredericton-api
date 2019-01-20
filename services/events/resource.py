from core.resource import ma
from marshmallow import fields, ValidationError
from services.events import constants


def validate_recurrence(val):
    if not constants.RecurrenceType.has_value(val):
        raise ValidationError('Invalid value, must be one of {}'.format(constants.RecurrenceType.values()))


class RecurrenceDetails(ma.Schema):
    recurrence = fields.Str(required=True, validate=validate_recurrence)
    num_recurrences = fields.Int(required=True,
                                 validate=lambda val: constants.MIN_RECURRENCE <= val <= constants.MAX_RECURRENCE)
    # day_of_week = fields.Int(required=False, validate=lambda val: 1 <= val <= 7)
    # week_of_month = fields.Int(required=False, validate=lambda val: 1 <= val <= 4)
    # day_of_month = fields.Int(required=False, validate=lambda val: 1 <= val <= 31)
    # days_of_week = fields.List(fields.Int(), validate=lambda val: 1 <= val <= 7, required=False)

    class Meta:
        strict = True


class EventSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    owner = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    categories = fields.List(fields.Str, missing=[])
    start_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(required=True, format=constants.EVENT_DATE_FORMAT)
    start_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)
    end_time = fields.DateTime(required=True, format=constants.EVENT_TIME_FORMAT)

    class Meta:
        strict = True


class EventListSchema(EventSchema):
    occurrence_num = fields.Int(dump_only=True)

    class Meta:
        strict = True


class EventDetailsSchema(EventSchema):
    is_recurring = fields.Bool(missing=False)
    recurrence_details = fields.Nested(RecurrenceDetails, required=False)
    timezone = fields.Str(dump_only=True)

    class Meta:
        strict = True


class EventOccurrenceDetailsSchema(EventDetailsSchema):
    occurrence_num = fields.Int(dump_only=True)

    class Meta:
        strict = True


class EventUpdateSchema(ma.Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    categories = fields.List(fields.Str, missing=[])
    start_date = fields.DateTime(required=False, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(required=False, format=constants.EVENT_DATE_FORMAT)
    start_time = fields.DateTime(required=False, format=constants.EVENT_TIME_FORMAT)
    end_time = fields.DateTime(required=False, format=constants.EVENT_TIME_FORMAT)
    is_recurring = fields.Bool(required=False)
    recurrence_details = fields.Nested(RecurrenceDetails, required=False)

    class Meta:
        strict = True


class EventFiltersSchema(ma.Schema):
    start_date = fields.DateTime(required=False, missing=None, format=constants.EVENT_DATE_FORMAT)
    end_date = fields.DateTime(required=False, missing=None, format=constants.EVENT_DATE_FORMAT)
    categories = fields.Str(required=False, missing=None)

    class Meta:
        strict = True


event_list_schema = EventListSchema()
event_details_schema = EventDetailsSchema()
event_occurrence_details_schema = EventOccurrenceDetailsSchema()
event_filters_schema = EventFiltersSchema()
event_update_schema = EventUpdateSchema()

