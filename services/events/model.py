from core.model import BaseModel
from pynamodb.attributes import BooleanAttribute, JSONAttribute, UnicodeAttribute


class EventModel(BaseModel):
    class Meta:
        simple_name = 'event'
        region = BaseModel.Meta.default_region

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)

    # contact_details = JSONAttribute(null=True)
    # is_verified = BooleanAttribute(default=False)