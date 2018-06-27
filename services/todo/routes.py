from flask import Blueprint, jsonify
from .model import TodoModel
from .resource import todo_schema
from webargs.flaskparser import use_kwargs

import logging
logger = logging.getLogger(__name__)
blueprint = Blueprint('todo', __name__)


@blueprint.route('/todos', methods=["GET"])
def list_todo_items():
    todo_items = TodoModel.scan()

    response = []

    for item in todo_items:
        response.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'is_complete': item.is_complete
        })

    return jsonify(response)


@blueprint.route('/todos', methods=["POST"])
@use_kwargs(todo_schema, locations=('json',))
def add_todo_item(**kwargs):
    todo_item = TodoModel(id=kwargs['id'],
                          title=kwargs['title'],
                          description=kwargs['description'],
                          is_complete=False)

    todo_item.save()

    response = jsonify(todo_schema.dump(todo_item).data)
    response.status_code = 201

    return response