from core.resource import ma
from marshmallow import fields


class OrganizationSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=False)


organization_schema = OrganizationSchema()
