from core import db
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from services.events.model import EventModel
from services.events.resource import event_schema
from services.organizations.utils import get_organization_from_db

blueprint = Blueprint('events', __name__)


@blueprint.route('/events', methods=["GET"])
def list_organizations():
    events_list = EventModel.scan()
    response = []

    for event in events_list:
        response.append(event_schema.dump(event).data)

    return jsonify(response)


@blueprint.route('/organizations/<org_id>/events', methods=["POST"])
@use_kwargs(event_schema, locations=('json',))
def create_organization_event(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    kwargs['owner'] = organization.id

    return create_event(**kwargs)


def create_event(**kwargs):
    event = EventModel(**kwargs)
    db.save_with_unique_id(event)

    response = jsonify(event_schema.dump(event).data)
    response.status_code = 201
    return response
