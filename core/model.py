import pendulum
from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute


def get_time_now():
    return pendulum.now().in_timezone('UTC')


class BaseModel(Model):
    class Meta:
        abstract = True
        default_region = 'ca-central-1'

    created = UTCDateTimeAttribute(default=get_time_now())
    updated = UTCDateTimeAttribute(default=get_time_now())

    @staticmethod
    def get_current_time():
        return get_time_now()

