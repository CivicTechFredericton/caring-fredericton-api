from core.resource import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    organization_id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    active = fields.Bool(dump_only=True)
    
    class Meta:
        strict = True

class UserListFiltersSchema(ma.Schema):

    class Meta:
        strict = True

user_schema = UserSchema()
user_list_filter_schema = UserListFiltersSchema()
