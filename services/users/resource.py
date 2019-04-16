from core.resource import ma
from marshmallow import fields


class BasicUserSchema(ma.Schema):
    class Meta:
        strict = True

    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    

class UserRegistrationSchema(BasicUserSchema):
    class Meta:
        strict = True

    password = fields.Str(load_only=True)


class UserDisplaySchema(BasicUserSchema):
    class Meta:
        strict = True

    id = fields.Str(dump_only=True)
    organization_id = fields.Str(dump_only=True)
    active = fields.Bool(dump_only=True)


class UserJoinOrgSchema(ma.Schema):
    class Meta:
        strict = True

    reason = fields.Str(required=True)


user_registration_schema = UserRegistrationSchema()
user_display_schema = UserDisplaySchema()
user_join_org_schema = UserJoinOrgSchema()
