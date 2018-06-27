from marshmallow import fields
from core.resource import ma


class ErrorSchema(ma.Schema):
    code = fields.Str()
    message = fields.Str()


ERROR_SCHEMA = ErrorSchema()
