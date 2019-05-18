from core.db.model import BaseModel
from pynamodb.attributes import BooleanAttribute, JSONAttribute, MapAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection, KeysOnlyProjection


class SearchNameIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'search_name-index'
        projection = KeysOnlyProjection()
        read_capacity_units = 0
        write_capacity_units = 0

    search_name = UnicodeAttribute(hash_key=True)


class OrganizationModel(BaseModel):
    class Meta(BaseModel.Meta):
        simple_name = 'organization'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    search_name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone = UnicodeAttribute()
    administrator_id = UnicodeAttribute() 
    address = JSONAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
    search_name_index = SearchNameIndex()

    def save(self, conditional_operator=None, **expected_values):
        self.search_name = self.name.lower()
        super().save(conditional_operator, **expected_values)
