from core.resource import ma
from marshmallow import fields


class ContactSchema(ma.Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(missing="")

    class Meta:
        strict = True


class OrganizationSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(missing="")
    is_verified = fields.Bool(dump_only=True)

    class Meta:
        strict = True


class OrganizationDetailsSchema(OrganizationSchema):
    contact_details = fields.Nested(ContactSchema, required=True)

    class Meta:
        strict = True


organization_schema = OrganizationSchema()
organization_details_schema = OrganizationDetailsSchema()
