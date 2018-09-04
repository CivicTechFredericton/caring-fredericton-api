from core.resource import ma
from marshmallow import fields


class OrganizationSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")

    class Meta:
        strict = True


organization_schema = OrganizationSchema()
