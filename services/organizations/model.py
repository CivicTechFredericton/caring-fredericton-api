from core.model import BaseModel
from pynamodb.attributes import BooleanAttribute, JSONAttribute, UnicodeAttribute


class OrganizationModel(BaseModel):
    class Meta:
        simple_name = 'organization'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    contact_details = JSONAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
