from core import errors
from core.db.events.model import EventModel


def get_event_from_db(event_id, owner):
    try:
        return EventModel.get(hash_key=event_id, range_key=owner)
    except EventModel.DoesNotExist:
        message = 'Event {} for owner {} does not exist'.format(event_id, owner)
        raise errors.ResourceValidationError(messages={'event': [message]})
