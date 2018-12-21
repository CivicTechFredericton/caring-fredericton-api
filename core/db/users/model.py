from core.db.model import BaseModel
from pynamodb import attributes, indexes


class UserEmail(indexes.GlobalSecondaryIndex):
    class Meta:
        simple_name = 'user-email-index'
        projection = indexes.IncludeProjection(['id'])

    email = attributes.UnicodeAttribute(hash_key=True)


class UserModel(BaseModel):
    class Meta:
        simple_name = 'user'
        region = BaseModel.Meta.default_region

    id = attributes.UnicodeAttribute(hash_key=True)
    username = attributes.UnicodeAttribute()
    organization_id = attributes.UnicodeAttribute()
    email = attributes.UnicodeAttribute()
    first_name = attributes.UnicodeAttribute()
    last_name = attributes.UnicodeAttribute()
    active = attributes.BooleanAttribute(default=True)
    user_email_index = UserEmail()

    def save(self, *args, **kwargs):
        self.username = self.email = self.email.lower()
        super().save(*args, **kwargs)