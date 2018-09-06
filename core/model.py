from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute


class BaseModel(Model):
    created = UTCDateTimeAttribute(default=datetime.now())
    updated = UTCDateTimeAttribute(default=datetime.now())
