import pendulum

from core.resource import ma
# from datetime import datetime
# from dateutil.parser import parse
# from dateutil.tz import tzutc
from marshmallow import fields


def get_time_now():
    return pendulum.now().in_timezone('UTC')


class EventSchema(ma.Schema):
    # def __init__(self):
      #   now = pendulum.now().in_timezone('UTC')

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    start_date = fields.Date(dump_only=True, default=get_time_now().to_date_string())
    end_date = fields.Date(dump_only=True, default=get_time_now().to_date_string())
    start_time = fields.Time(dump_only=True, default=get_time_now().to_time_string())
    end_time = fields.Time(dump_only=True, default=get_time_now().to_time_string())
    timezone = fields.Str(dump_only=True, default=get_time_now().timezone_name)

    class Meta:
        strict = True


class EventInputSchema(EventSchema):
    full_start_date = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S')
    full_end_date = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        strict = True


class EventDetailsSchema(EventSchema):
    start_date = fields.Date(dump_only=True, default=get_time_now().to_date_string())
    end_date = fields.Date(dump_only=True, default=get_time_now().to_date_string())
    start_time = fields.Time(dump_only=True, default=get_time_now().to_time_string())
    end_time = fields.Time(dump_only=True, default=get_time_now().to_time_string())

    class Meta:
        strict = True

event_schema = EventSchema()

