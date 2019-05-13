from core.db.model import BaseModel
from pynamodb.attributes import BooleanAttribute, JSONAttribute, MapAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection, KeysOnlyProjection


class OrganizationNameIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'name-index'
        projection = KeysOnlyProjection()

    name = UnicodeAttribute(hash_key=True)


class OrganizationModel(BaseModel):
    class Meta(BaseModel.Meta):
        simple_name = 'organization'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone = UnicodeAttribute()
    administrator_id = UnicodeAttribute() 
    address = JSONAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
    organization_name_index = OrganizationNameIndex()
