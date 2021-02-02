from marshmallow import Schema, fields


class ErrorSchema(Schema):
    code = fields.Str()
    message = fields.Str()

    class Meta:
        strict = True


ERROR_SCHEMA = ErrorSchema()
