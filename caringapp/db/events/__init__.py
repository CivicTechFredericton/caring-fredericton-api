from caringapp.core import errors
from caringapp.db.events.model import EventModel


def get_event_from_db(event_id, owner):
    try:
        return EventModel.get(hash_key=event_id, range_key=owner)
    except EventModel.DoesNotExist:
        message = 'Event {} for owner {} does not exist'.format(event_id, owner)
        raise errors.ResourceNotFoundError(messages={'event': [message]})


def remove_event_from_db(event_id, owner):
    event = get_event_from_db(event_id, owner)

    try:
        # TODO: Soft delete vs hard delete?
        event.delete()
    except EventModel.DeleteError:
        message = 'Unable to delete event {} for owner {}'.format(event_id, owner)
        raise errors.BadRequestError(messages={'event': [message]})
