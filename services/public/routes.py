"""
This class holds end points which are used for guest access
"""

from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.events import EventModel
from services.events.resource import event_filters_schema

blueprint = Blueprint('public', __name__)


@blueprint.route('/events', methods=["GET"])
@use_kwargs(event_filters_schema, locations=('query',))
def list_events(**kwargs):
    """
    List the events in the system agnostic to any owner
    :return: The list of events in the system
    """
    events_list = EventModel.scan()
    return get_events_response(events_list, **kwargs)
