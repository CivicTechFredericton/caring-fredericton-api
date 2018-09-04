from core.resource import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)  # read-only (won't be parsed by webargs)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)  # write-only
    first_name = fields.Str(missing="")
    last_name = fields.Str(missing="")
    date_registered = fields.DateTime(dump_only=True)

    class Meta:
        strict = True


user_schema = UserSchema()