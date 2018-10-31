from core.resource import ma
from marshmallow import fields
from services.events import constants


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

    class Meta:
        strict = True


event_schema = EventSchema()

