from core import db
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from services.events.model import EventModel
from services.events.resource import event_schema
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
@use_kwargs(event_schema, locations=('json',))
def create_organization_event(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    kwargs['owner'] = organization.id

    return create_event(**kwargs)


def get_events_response(events_list):
    response = []

    for event in events_list:
        response.append(event_schema.dump(event).data)

    return jsonify(response)


def create_event(**kwargs):
    event = EventModel(**kwargs)
    db.save_with_unique_id(event)

    response = jsonify(event_schema.dump(event).data)
    response.status_code = 201
    return response
