"""
This class holds end points which are used for guest access
"""

from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.events import get_event_from_db
from core.db.events.model import EventModel
from core.db.organizations.model import OrganizationModel
from services.events import get_event_occurrence
from services.events.resource import event_filters_schema, event_occurrence_details_schema
from services.events.routes import get_events_response
from services.guest import build_list_events_scan_condition
from services.guest.resource import event_details_filter_schema, organization_list_schema

blueprint = Blueprint('guest', __name__)


# -------------------------
# Organization End Points
# -------------------------
@blueprint.route('/guests/organizations', methods=["GET"])
def list_verified_organizations():
    organizations = OrganizationModel.scan(OrganizationModel.is_verified == True)
    response = [organization_list_schema.dump(org) for org in organizations]

    return jsonify(response)


# -------------------------
# Events End Points
# -------------------------
@blueprint.route('/guests/events', defaults={'org_id': None}, methods=["GET"])
@blueprint.route('/guests/organizations/<org_id>/events', methods=["GET"])
@use_kwargs(event_filters_schema, locations=('query',))
def list_events(org_id, **kwargs):
    scan_condition = build_list_events_scan_condition(org_id)
    events_list = EventModel.scan(scan_condition)
    return get_events_response(events_list, **kwargs)


@blueprint.route('/guests/organizations/<org_id>/events/<event_id>', methods=["GET"])
@use_kwargs(event_details_filter_schema, locations=('query',))
def get_organization_event(org_id, event_id, **kwargs):
    event = get_event_from_db(event_id, org_id)
    occurrence = get_event_occurrence(event, kwargs.get('occurrence_num'))
    return jsonify(event_occurrence_details_schema.dump(occurrence))

