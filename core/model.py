import pendulum

from core.auth import get_current_user_id
from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute

import logging
logger = logging.getLogger(__name__)


def get_time_now():
    return pendulum.now().in_timezone('UTC')


class BaseModel(Model):
    class Meta:
        abstract = True
        default_region = 'ca-central-1'

    # created_at = NumberAttribute()
    created_at = UTCDateTimeAttribute()
    created_by = UnicodeAttribute()
    # updated_at = NumberAttribute()
    updated_at = UTCDateTimeAttribute()
    updated_by = UnicodeAttribute()

    def save(self, *args, **kwargs):
        timestamp = get_time_now()
        current_user = get_current_user_id()

        if self.created_at is None or self.created_by is None:
            logger.debug('First time save of entity; setting created_at and created_by', extra={
                'CreatedAt': timestamp,
                'CreatedBy': current_user,
            })

            self.created_at = timestamp
            self.created_by = current_user

        self.updated_at = timestamp
        self.updated_by = current_user

        return Model.save(self, *args, **kwargs)

    def update(self, attributes=None, actions=None, condition=None, conditional_operator=None, **expected_values):
        # Set the updated_at and updated_by values
        actions.append(BaseModel.updated_at.set(get_time_now()))
        actions.append(BaseModel.updated_by.set(get_current_user_id()))

        return Model.update(self, attributes, actions, condition, conditional_operator, **expected_values)

    # @staticmethod
    # def get_current_time():
    #     return get_time_now()

