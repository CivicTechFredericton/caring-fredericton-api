from core.resource import ma
from marshmallow import fields

class UserEntrySchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    
    class Meta:
        strict = True

class UserDisplaySchema(ma.Schema):
    id = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    organization_id = fields.Str(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)	
    active = fields.Bool(dump_only=True)
    
    class Meta:
	    strict = True

class UserListFiltersSchema(ma.Schema):

    class Meta:
        strict = True

user_entry_schema = UserEntrySchema()
user_display_schema = UserDisplaySchema()
user_list_filter_schema = UserListFiltersSchema()
