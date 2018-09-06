from core.model import BaseModel
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute


class OrganizationModel(BaseModel):
    class Meta:
        simple_name = 'organization'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
