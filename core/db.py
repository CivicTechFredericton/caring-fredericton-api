from pynamodb import indexes
from services.todo.model import TodoModel

import logging
logger = logging.getLogger(__name__)

# List for all PynamoDB models (both index and tables)
MODELS = [TodoModel]


def init_models(service_name, stage, host=None):
    logger.info("Configuring pynamodb models. host: %s", host)

    for model in MODELS:
        model.Meta.host = host

        model.Meta.index_name = model.Meta.table_name = \
            '{}-{}-{}'.format(service_name, stage, model.Meta.simple_name)

        entity_type = 'index' if isinstance(model, indexes.Index) else 'table'
        logger.debug("Init %s model '%s'", entity_type, model.Meta.index_name)
