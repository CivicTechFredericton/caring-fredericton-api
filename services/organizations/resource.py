from core.resource import ma
from marshmallow import fields


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


# administrator is now specified by email  
class OrganizationDetailsSchema(OrganizationSchema):
    administrator_email = fields.Email(required=True)
    address = fields.Nested(AddressSchema, required=True)

    class Meta:
        strict = True


class OrganizationUpdateSchema(ma.Schema):
    name = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    address = fields.Nested(AddressSchema)

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
organization_update_schema = OrganizationUpdateSchema()
organization_verification_schema = OrganizationVerificationSchema()
