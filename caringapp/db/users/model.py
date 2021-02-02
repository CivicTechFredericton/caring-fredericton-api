from pynamodb.attributes import BooleanAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

from caringapp.db.model import BaseModel


class UserEmail(GlobalSecondaryIndex):
    class Meta:
        index_name = 'user-email-index'
        projection = KeysOnlyProjection()
        read_capacity_units = 0
        write_capacity_units = 0

    email = UnicodeAttribute(hash_key=True)


class UserModel(BaseModel):
    class Meta(BaseModel.Meta):
        simple_name = 'user'

    id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    active = BooleanAttribute(default=True)
    organization_id = UnicodeAttribute(null=True)
    organization_name = UnicodeAttribute(null=True)
    user_email_index = UserEmail()
