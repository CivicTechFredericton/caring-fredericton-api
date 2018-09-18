from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute


class BaseModel(Model):
    class Meta:
        abstract = True
        default_region = 'ca-central-1'

    created = UTCDateTimeAttribute(default=datetime.now())
    updated = UTCDateTimeAttribute(default=datetime.now())
