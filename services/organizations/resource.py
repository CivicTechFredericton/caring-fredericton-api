from core.resource import ma
from marshmallow import fields


class AdminSchema(ma.Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)

    class Meta:
        strict = True


class AddressSchema(ma.Schema):
    street = fields.Str(required=True)
    postal_code = fields.Str(required=True)
    city = fields.Str(required=True)
    province = fields.Str(required=True)
    country = fields.Str(required=True)

    class Meta:
        strict = True


class OrganizationListFiltersSchema(ma.Schema):
    is_verified = fields.Bool(required=False)

    class Meta:
        strict = True


class OrganizationSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    is_verified = fields.Bool(dump_only=True)
    
    class Meta:
        strict = True


class OrganizationDetailsSchema(OrganizationSchema):
    administrator = fields.Nested(AdminSchema, required=True)
    address = fields.Nested(AddressSchema, required=True)

    class Meta:
        strict = True


class OrganizationVerificationSchema(ma.Schema):
    is_verified = fields.Bool(required=True)
    reason = fields.Str(required=False)

    class Meta:
        strict = True


organization_schema = OrganizationSchema()
organization_list_filters_schema = OrganizationListFiltersSchema()
organization_details_schema = OrganizationDetailsSchema()
organization_verification_schema = OrganizationVerificationSchema()
