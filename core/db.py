import uuid

from pynamodb import indexes
from pynamodb.exceptions import PutError
from services.events.model import EventModel
from services.organizations.model import OrganizationModel

import logging
logger = logging.getLogger(__name__)

# List for all PynamoDB models (both index and tables)
MODELS = [EventModel, OrganizationModel]


def init_models(service_name, stage, host=None):
    logger.info("Configuring pynamodb models. host: %s", host)

    for model in MODELS:
        model.Meta.host = host

        model.Meta.index_name = model.Meta.table_name = \
            '{}-{}-{}'.format(service_name, stage, model.Meta.simple_name)

        entity_type = 'index' if isinstance(model, indexes.Index) else 'table'
        logger.debug("Init %s model '%s'", entity_type, model.Meta.index_name)


def save_with_unique_id(item):
    """
    Save a record in the database using a unique identifier value
    :param item: The item to be saved
    :return: None
    """
    item.id = str(uuid.uuid4())
    try:
        item.save(id__null=True)
    except PutError as e:
        logger.error('Unable to save the item {}'.format(str(e)))
