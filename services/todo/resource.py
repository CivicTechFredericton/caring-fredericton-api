from core.resource import ma
from marshmallow import fields


class TodoSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=False)


todo_schema = TodoSchema()
