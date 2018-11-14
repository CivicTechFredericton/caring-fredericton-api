from core import db, errors
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from services.events.model import EventModel
from services.events.resource import event_schema, event_details_schema
from services.events.utils import get_recurring_event, set_occurrences
from services.organizations.utils import get_organization_from_db

blueprint = Blueprint('events', __name__)


@blueprint.route('/events', methods=["GET"])
def list_events():
    """
    List the events in the system agnostic to any owner
    :return: The list of events in the system
    """
    events_list = EventModel.scan()
    return get_events_response(events_list)


@blueprint.route('/organizations/<org_id>/events', methods=["GET"])
def list_events_for_organization(org_id):
    """
    Returns the list of events for an organization
    :param org_id: The organization identifier
    :return: The list of events associated to the organization
    """
    events_list = EventModel.scan(EventModel.owner == org_id)
    return get_events_response(events_list)


@blueprint.route('/organizations/<org_id>/events', methods=["POST"])
@use_kwargs(event_details_schema, locations=('json',))
def create_organization_event(org_id, **kwargs):
    event_args = {k: v for k, v in kwargs.items() if v is not None}

    organization = get_organization_from_db(org_id)
    event_args['owner'] = organization.id

    return create_event(**event_args)


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=["PUT"])
@use_kwargs(event_details_schema, locations=('json',))
def update_organization_event(org_id, event_id, **kwargs):
    event = get_event_from_db(event_id, org_id)
    event.update(
        actions=[
            EventModel.name.set(kwargs['name']),
            EventModel.description.set(kwargs['description']),
            EventModel.start_date.set(kwargs['start_date']),
            EventModel.end_date.set(kwargs['end_date']),
            EventModel.start_time.set(kwargs['start_time']),
            EventModel.end_time.set(kwargs['end_time']),
            EventModel.updated.set(EventModel.get_current_time())
        ]
    )

    return jsonify(event_details_schema.dump(event).data)


def get_events_response(events_list):
    response = []

    # Filter the list of events
    for event in events_list:
        occurrences = event.occurrences
        if occurrences is not None:
            # Include the recurring events
            for val in occurrences:
                add_to_response_list(response, get_recurring_event(event, val))
        else:
            add_to_response_list(response, event)

    return jsonify(response)


# ----------------------------------------------------
# Helper Functions
# ----------------------------------------------------
def create_event(**event_args):
    # Set the number of occurrences
    set_occurrences(event_args)

    # Save the object
    event = EventModel(**event_args)
    db.save_with_unique_id(event)

    response = jsonify(event_details_schema.dump(event).data)
    response.status_code = 201
    return response


def get_event_from_db(event_id, owner):
    try:
        return EventModel.get(hash_key=event_id, range_key=owner)
    except EventModel.DoesNotExist:
        message = 'Event {} for owner {} does not exist'.format(event_id, owner)
        raise errors.ResourceValidationError(messages={'event': [message]})


def add_to_response_list(response, event):
    response.append(event_schema.dump(event).data)
