from marshmallow import fields
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class PagedSchema(ma.Schema):
    class Meta:
        fields = (
            '_links',
            'objects',
        )

    pages = fields.Integer(dump_to='pages', dump_only=True)
    limit = fields.Integer(dump_to='limit', dump_only=True)
    total = fields.Integer(dump_to='total', dump_only=True)
