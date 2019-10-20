import json

from datetime import datetime
from core.auth import get_current_user_id
from core.configuration import get_region_name, get_current_stage, get_service_name
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

import logging

from core.errors import ResourceNotFoundError
from core.utils import get_time_now

logger = logging.getLogger(__name__)


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
        table_name = None
        index_name = None

        def __init_subclass__(cls, **kwargs):
            cls.table_name = cls.get_table_name(cls)
            super().__init_subclass__(**kwargs)

        def get_table_name(self):
            if not self.index_name:
                service_name = get_service_name()
                stage_name = get_current_stage()
                simple_name = getattr(self, 'simple_name')

                self.index_name = self.table_name = '{}-{}-{}'.format(
                    service_name, stage_name, simple_name)

                logger.info("Init model '{}'".format(self.index_name))
            return self.index_name

    created_at = UTCDateTimeAttribute()
    created_by = UnicodeAttribute()
    updated_at = UTCDateTimeAttribute()
    updated_by = UnicodeAttribute()

    def save(self, conditional_operator=None):
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

        return Model.save(self, conditional_operator)

    def update(self, actions, condition=None):
        self.updated_at = get_time_now()
        self.updated_by = get_current_user_id()

        return Model.update(self, actions, condition)

    @classmethod
    def fetch(cls, *args, **kwargs):
        try:
            model = cls.get(*args, **kwargs)
            return model
        except cls.DoesNotExist:
            raise ResourceNotFoundError

    def to_dict(self):
        return json.loads(json.dumps(self, cls=ModelEncoder))
