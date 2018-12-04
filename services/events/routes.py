from core import db
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.events import get_event_from_db
from core.db.events.model import EventModel
from services.events import build_update_actions, get_recurring_events_list, set_filter_dates, set_occurrences
from services.events.resource import event_schema, event_details_schema, event_filters_schema
from core.db.organizations import get_organization_from_db

blueprint = Blueprint('events', __name__)


@blueprint.route('/events', methods=["GET"])
@use_kwargs(event_filters_schema, locations=('query',))
def list_events(**kwargs):
    """
    List the events in the system agnostic to any owner
    :return: The list of events in the system
    """
    events_list = EventModel.scan()
    return get_events_response(events_list, **kwargs)


@blueprint.route('/organizations/<org_id>/events', methods=["GET"])
@use_kwargs(event_filters_schema, locations=('query',))
def list_events_for_organization(org_id, **kwargs):
    """
    Returns the list of events for an organization
    :param org_id: The organization identifier
    :return: The list of events associated to the organization
    """
    events_list = EventModel.scan(EventModel.owner == org_id)
    return get_events_response(events_list, **kwargs)


@blueprint.route('/organizations/<org_id>/events', methods=["POST"])
@use_kwargs(event_details_schema, locations=('json',))
def create_organization_event(org_id, **kwargs):
    event_args = {k: v for k, v in kwargs.items() if v is not None}

    # Verify organization exists
    organization = get_organization_from_db(org_id)
    event_args['owner'] = organization.id

    return create_event(**event_args)


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=["GET"])
def get_organization_event(org_id, event_id):
    # TODO: Handle specific occurrence lookup
    event = get_event_from_db(event_id, org_id)
    return jsonify(event_details_schema.dump(event).data)


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=["PUT"])
@use_kwargs(event_details_schema, locations=('json',))
def update_organization_event(org_id, event_id, **kwargs):
    event = get_event_from_db(event_id, org_id)
    actions = build_update_actions(event, **kwargs)
    db.update_item(event, actions)

    return jsonify(event_details_schema.dump(event).data)


# ----------------------------------------------------
# Helper Functions
# ----------------------------------------------------
def get_events_response(events_list, **kwargs):
    response = []

    # categories = ['all', 'dinner', 'fund-raiser', 'service']
    # categories = []
    # test_list = ['aa', 'dds']
    # test_list = []
    # print(len([i for e in test_list for i in categories if e in i]))

    # Set the filters
    filter_start_date, filter_end_date = set_filter_dates(kwargs['start_date'], kwargs['end_date'])

    for event in events_list:
        occurrences = get_recurring_events_list(event, filter_start_date, filter_end_date)
        for occurrence in occurrences:
            response.append(event_schema.dump(occurrence).data)

    return jsonify(response)


def create_event(**event_args):
    # Set the number of occurrences
    set_occurrences(event_args)

    # Save the object
    event = EventModel(**event_args)
    db.save_with_unique_id(event)

    response = jsonify(event_details_schema.dump(event).data)
    response.status_code = 201
    return response
