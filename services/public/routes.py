"""
This class holds end points which are used for guest access
"""

from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.events import EventModel
from core.db.organizations import OrganizationModel
from services.events.resource import event_filters_schema
from services.events.routes import get_events_response
from services.public.resource import organization_list_schema

blueprint = Blueprint('public', __name__)


@blueprint.route('/organizations', methods=["GET"])
def list_verified_organizations():
    # filter_condition = build_filter_condition(**kwargs)
    organizations = OrganizationModel.scan(OrganizationModel.is_verified == True)

    response = [organization_list_schema.dump(org).data for org in organizations]
    #
    # for org in organizations:
    #     response.append(organization_list_schema.dump(org).data)

    return jsonify(response)


@blueprint.route('/events', methods=["GET"])
@use_kwargs(event_filters_schema, locations=('query',))
def list_events(**kwargs):
    """
    List the events in the system agnostic to any owner
    :return: The list of events in the system
    """
    events_list = EventModel.scan()
    return get_events_response(events_list, **kwargs)
