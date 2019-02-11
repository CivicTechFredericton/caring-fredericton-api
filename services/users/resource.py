from core.resource import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    id = fields.Str(dump_only=True)
    
    class Meta:
        strict = True

user_schema = UserSchema()
