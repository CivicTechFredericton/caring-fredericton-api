from core.model import BaseModel
from pynamodb.attributes import BooleanAttribute, JSONAttribute, UnicodeAttribute


class OrganizationModel(BaseModel):
    class Meta:
        simple_name = 'organization'
        region = BaseModel.Meta.default_region

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone = UnicodeAttribute()
    administrator = JSONAttribute(null=True)
    address = JSONAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
