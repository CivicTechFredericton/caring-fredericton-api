from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs
from .model import EventModel
from .resource import event_schema

blueprint = Blueprint('events', __name__)


@blueprint.route('/events', methods=["GET"])
def list_organizations():
    events_list = EventModel.scan()
    response = []

    for event in events_list:
        response.append(event_schema.dump(event).data)

    return jsonify(response)


@blueprint.route('/events', methods=["POST"])
@use_kwargs(event_schema, locations=('json',))
def create_event(**kwargs):
    return jsonify({
        "name": kwargs["name"],
        "description": kwargs["description"]
    })
