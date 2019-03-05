from core.resource import ma
from marshmallow import fields

# common public user info fields for all stages
class BasicUserSchema(ma.Schema):
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    
    class Meta:
        strict = True

# fields needed to register a user  
class UserRegistrationSchema(BasicUserSchema):
    password = fields.Str(required=True)
    
    class Meta:
        strict = True

# collection of all public fields for display  
class UserDisplaySchema(BasicUserSchema):
    id = fields.Str(dump_only=True)
    organization_id = fields.Str(dump_only=True)
    active = fields.Bool(dump_only=True)
    
    class Meta:
	    strict = True

# schema for activating a user by updating password
class UserActivationSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)

class UserListFiltersSchema(ma.Schema):

    class Meta:
        strict = True

user_registration_schema = UserRegistrationSchema()
user_display_schema = UserDisplaySchema()
user_activation_schema = UserActivationSchema()
user_list_filter_schema = UserListFiltersSchema()
