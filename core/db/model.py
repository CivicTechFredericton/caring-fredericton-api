import json

from datetime import datetime
from core.auth import get_current_user_id
from core.configuration import get_region_name
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

import logging
logger = logging.getLogger(__name__)


def get_time_now():
    return datetime.utcnow()


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'attribute_values'):
            return obj.attribute_values
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class BaseModel(Model):
    class Meta:
        abstract = True
        region = get_region_name()

    created_at = UTCDateTimeAttribute()
    created_by = UnicodeAttribute()
    updated_at = UTCDateTimeAttribute()
    updated_by = UnicodeAttribute()

    def save(self, conditional_operator=None, **expected_values):
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

        return Model.save(self, conditional_operator, **expected_values)

    def update(self, attributes=None, actions=None, condition=None, conditional_operator=None, **expected_values):
        # Set the updated_at and updated_by values
        self.updated_at = get_time_now()
        self.updated_by = get_current_user_id()

        return Model.update(self, attributes, actions, condition, conditional_operator, **expected_values)

    def to_dict(self):
        return json.loads(json.dumps(self, cls=ModelEncoder))
