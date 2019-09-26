from core.resource import ma
from marshmallow import fields


class AddressSchema(ma.Schema):
    class Meta:
        strict = True

    street = fields.Str(required=True)
    postal_code = fields.Str(required=True)
    city = fields.Str(required=True)
    province = fields.Str(required=True)
    country = fields.Str(required=True)


class AdministratorDetails(ma.Schema):
    class Meta:
        strict = True

    email = fields.Str(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)


class OrganizationListFiltersSchema(ma.Schema):
    class Meta:
        strict = True

    is_verified = fields.Bool(required=False)


class OrganizationSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    administrator_id = fields.Str(required=True)
    is_verified = fields.Bool(dump_only=True)


class OrganizationDetailsSchema(OrganizationSchema):
    class Meta:
        strict = True

    address = fields.Nested(AddressSchema, required=True)
    administrator_details = fields.Nested(AdministratorDetails, required=False)


class OrganizationUpdateSchema(ma.Schema):
    class Meta:
        strict = True

    name = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    address = fields.Nested(AddressSchema)


class OrganizationVerificationSchema(ma.Schema):
    class Meta:
        strict = True

    is_verified = fields.Bool(required=True)
    reason = fields.Str(required=False)


organization_schema = OrganizationSchema()
organization_list_filters_schema = OrganizationListFiltersSchema()
organization_details_schema = OrganizationDetailsSchema()
organization_update_schema = OrganizationUpdateSchema()
organization_verification_schema = OrganizationVerificationSchema()
