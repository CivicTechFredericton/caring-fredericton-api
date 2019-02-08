from core import db
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.events import remove_event_from_db, get_event_from_db
from core.db.events.model import EventModel
from services.events import build_list_events_scan_condition, build_update_actions, create_event, \
    get_event_occurrence, get_recurring_events_list, set_dates_filter, set_category_filter, update_event_occurrences
from services.events.resource import event_details_schema, event_details_filter_schema, event_filters_schema, \
    event_list_schema, event_occurrence_details_schema, event_occurrence_update_schema, event_update_schema
from core.db.organizations import get_verified_organization_from_db

blueprint = Blueprint('events', __name__)


@blueprint.route('/events', defaults={'org_id': None}, methods=["GET"])
@blueprint.route('/organizations/<org_id>/events', methods=["GET"])
@use_kwargs(event_filters_schema, locations=('query',))
def list_events(org_id, **kwargs):
    scan_condition = build_list_events_scan_condition(org_id)
    events_list = EventModel.scan(scan_condition)
    return get_events_response(events_list, **kwargs)


@blueprint.route('/organizations/<org_id>/events', methods=["POST"])
@use_kwargs(event_details_schema, locations=('json',))
def create_organization_event(org_id, **kwargs):
    event_args = {k: v for k, v in kwargs.items() if v is not None}

    organization = get_verified_organization_from_db(org_id)
    event_args['owner'] = organization.id

    event = create_event(**event_args)
    response = jsonify(event_details_schema.dump(event).data)
    response.status_code = 201

    return response


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=["GET"])
@use_kwargs(event_details_filter_schema, locations=('query',))
def get_organization_event(org_id, event_id, **kwargs):
    event = get_event_from_db(event_id, org_id)
    occurrence = get_event_occurrence(event, kwargs.get('occurrence_num'))
    return jsonify(event_occurrence_details_schema.dump(occurrence).data)


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=["PUT"])
@use_kwargs(event_update_schema, locations=('json',))
def update_organization_event(org_id, event_id, **kwargs):
    event_args = {k: v for k, v in kwargs.items() if v is not None}

    event = get_event_from_db(event_id, org_id)
    actions = build_update_actions(event, event_args)
    db.update_item(event, actions)

    return jsonify(event_details_schema.dump(event).data)


@blueprint.route('/organizations/<org_id>/events/<event_id>', methods=['DELETE'])
def cancel_organization_event(org_id, event_id):
    remove_event_from_db(event_id, org_id)

    return '', 204


@blueprint.route('/organizations/<org_id>/events/<event_id>/change-occurrence', methods=["PUT"])
@use_kwargs(event_occurrence_update_schema, locations=('json',))
def update_organization_event_occurrences(org_id, event_id, **kwargs):
    event_args = {k: v for k, v in kwargs.items() if v is not None}

    event = get_event_from_db(event_id, org_id)
    update_event_occurrences(event, event_args)

    # TODO: Update response
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
