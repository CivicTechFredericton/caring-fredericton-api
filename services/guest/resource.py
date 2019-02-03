from core.resource import ma
from marshmallow import fields


class OrganizationListSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)

    class Meta:
        strict = True


class EventDetailsFilterSchema(ma.Schema):
    occurrence_num = fields.Int(missing=1)

    class Meta:
        strict = True


organization_list_schema = OrganizationListSchema()
event_details_filter_schema = EventDetailsFilterSchema()
