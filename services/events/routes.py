from flask import Blueprint, jsonify
from .model import EventModel
from .resource import event_schema

blueprint = Blueprint('organizations', __name__)


@blueprint.route('/events', methods=["GET"])
def list_organizations():
    events_list = EventModel.scan()
    response = []

    for event in events_list:
        response.append(event_schema.dump(event).data)

    return jsonify(response)
