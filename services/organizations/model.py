from pynamodb.models import Model
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute


class OrganizationModel(Model):
    class Meta:
        simple_name = 'organization'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
    # TODO: Enable time stamps
    # created = UTCDateTimeAttribute()
    # updated = UTCDateTimeAttribute()
