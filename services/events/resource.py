from core.resource import ma
from marshmallow import fields


class EventSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    # start_date = fields.Date(required=False)
    # end_date = fields.Date(required=False)
    # start_time = fields.Time(required=False)
    # end_time = fields.Time(required=False)

    class Meta:
        strict = True


event_schema = EventSchema()
