from marshmallow import fields, Schema


class OrganizationListSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)

    class Meta:
        strict = True


class EventDetailsFilterSchema(Schema):
    occurrence_num = fields.Int(missing=1)

    class Meta:
        strict = True


organization_list_schema = OrganizationListSchema()
event_details_filter_schema = EventDetailsFilterSchema()
