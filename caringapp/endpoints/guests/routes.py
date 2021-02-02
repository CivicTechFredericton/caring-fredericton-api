"""
This class holds end points which are used for guests access
"""

from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from caringapp.db.events import get_event_from_db
from caringapp.db.events.model import EventModel
from services.events import get_event_occurrence
from services.events.resource import event_filters_schema, event_occurrence_details_schema
from services.events.routes import get_events_response
from services.guest import build_list_events_scan_condition
from services.guest.resource import event_details_filter_schema

blueprint = Blueprint('guests', __name__)


# -------------------------
# Events End Points
# -------------------------
@blueprint.route('/guests/events', defaults={'org_id': None}, methods=["GET"])
@use_kwargs(event_filters_schema, location='query')
def list_events(org_id, **kwargs):
    scan_condition = build_list_events_scan_condition(org_id)
    events_list = EventModel.scan(scan_condition)
    return get_events_response(events_list, **kwargs)


@blueprint.route('/guests/organizations/<org_id>/events/<event_id>', methods=["GET"])
@use_kwargs(event_details_filter_schema, location='query')
def get_organization_event(org_id, event_id, **kwargs):
    event = get_event_from_db(event_id, org_id)
    occurrence = get_event_occurrence(event, kwargs.get('occurrence_num'))
    return jsonify(event_occurrence_details_schema.dump(occurrence))

