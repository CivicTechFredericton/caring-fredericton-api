import uuid

from pynamodb.exceptions import PutError

import logging
logger = logging.getLogger(__name__)


def get_filter_condition(conditions):
    filter_condition = None

    for index, condition in enumerate(conditions):
        if index == 0:
            filter_condition = condition
        else:
            filter_condition = filter_condition & condition

    return filter_condition


def update_item(item, actions):
    if actions:
        item.update(actions=actions)
    else:
        logger.info('Item not changed on update')


def save_with_unique_id(item):
    """
    Save a record in the database using a unique identifier value
    :param item: The item to be saved
    :return: None
    """
    item.id = str(uuid.uuid4())
    return save_item(item)


def save_item(item):
    """
    Save a record in the database
    :param item: The item to be saved
    :return:
    """
    try:
        item.save()
    except PutError as e:
        logger.error('Unable to save the item {}'.format(str(e)))

