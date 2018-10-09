# from datetime import datetime
import pendulum
from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute


class BaseModel(Model):
    class Meta:
        abstract = True
        default_region = 'ca-central-1'

    created = UTCDateTimeAttribute(default=pendulum.now())
    updated = UTCDateTimeAttribute(default=pendulum.now())
