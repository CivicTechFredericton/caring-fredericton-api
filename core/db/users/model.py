from core.db.model import BaseModel
from pynamodb import attributes, indexes


class UserEmail(indexes.GlobalSecondaryIndex):
    class Meta:
        index_name = 'user-email-index'
        projection = indexes.KeysOnlyProjection()

    email = attributes.UnicodeAttribute(hash_key=True)


class UserModel(BaseModel):
    class Meta(BaseModel.Meta):
        simple_name = 'user'

    id = attributes.UnicodeAttribute(hash_key=True)
    email = attributes.UnicodeAttribute()
    organization_id = attributes.UnicodeAttribute(null=True)
    first_name = attributes.UnicodeAttribute()
    last_name = attributes.UnicodeAttribute()
    active = attributes.BooleanAttribute(default=False)
    user_email_index = UserEmail()

    def save(self, *args, **kwargs):
        self.email = str(self.email).lower()
        super().save(*args, **kwargs)
