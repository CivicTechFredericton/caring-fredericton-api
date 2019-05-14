from core.db.model import BaseModel
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection


class UserEmail(GlobalSecondaryIndex):
    class Meta:
        index_name = 'user-email-index'
        projection = KeysOnlyProjection()

    email = UnicodeAttribute(hash_key=True)


class UserModel(BaseModel):
    class Meta(BaseModel.Meta):
        simple_name = 'user'

    id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    organization_id = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    active = BooleanAttribute(default=True)
    user_email_index = UserEmail()
