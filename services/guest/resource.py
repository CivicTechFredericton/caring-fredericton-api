from core.resource import ma
from marshmallow import fields


class OrganizationListSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)

    class Meta:
        strict = True


organization_list_schema = OrganizationListSchema()
