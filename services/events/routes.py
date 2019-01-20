from core import db
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.events import get_event_from_db
from core.db.events.model import EventModel
from services.events import build_update_actions, get_event_occurrence, get_recurring_events_list, \
    set_dates_filter, set_category_filter, set_occurrences
from services.events.resource import event_details_schema, event_filters_schema, \
    event_list_schema, event_occurrence_details_schema, event_update_schema
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
    event = get_event_from_db(event_id, org_id)
    # occurrence = get_event_occurrence(event)
    return jsonify(event_details_schema.dump(event).data)


@blueprint.route('/organizations/<org_id>/events/<event_id>/occurrence/<int:occurrence>', methods=["GET"])
def get_event_occurrence_details(org_id, event_id, occurrence):
    event = get_event_from_db(event_id, org_id)
    occurrence = get_event_occurrence(event, occurrence)
    return jsonify(event_occurrence_details_schema.dump(occurrence).data)


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=["PUT"])
@use_kwargs(event_update_schema, locations=('json',))
def update_organization_event(org_id, event_id, **kwargs):
    event = get_event_from_db(event_id, org_id)

    event_args = {k: v for k, v in kwargs.items() if v is not None}
    actions = build_update_actions(event, event_args)
    db.update_item(event, actions)

    return jsonify(event_details_schema.dump(event).data)


@blueprint.route('/organizations/<org_id>/events/<event_id>/change-occurrence', methods=["PUT", "PATCH"])
def update_event_occurrences(org_id, event_id):
    event = get_event_from_db(event_id, org_id)
    from services.events import update_event_occurrences
    update_event_occurrences(event)

    # Read in the updated event details

    # occurrence_option = 'THIS_EVENT'
    # occurrence_option = 'REMAINING_EVENTS'
    # new_start_date, new_end_date, new start_time, new_end_time

    # If change to this event only, perform update on current event to

    return jsonify(event_details_schema.dump(event).data)


# ----------------------------------------------------
# Helper Functions
# ----------------------------------------------------
def get_events_response(events_list, **kwargs):
    # Set the filters
    filter_start_date, filter_end_date = set_dates_filter(kwargs['start_date'], kwargs['end_date'])
    filter_categories = set_category_filter(kwargs['categories'])

    response = []
    for event in events_list:
        occurrences = get_recurring_events_list(event, filter_start_date, filter_end_date, filter_categories)
        for occurrence in occurrences:
            response.append(event_list_schema.dump(occurrence).data)

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
