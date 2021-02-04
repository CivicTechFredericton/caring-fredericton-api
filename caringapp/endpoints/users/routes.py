from flask import Blueprint, jsonify

from caringapp.db.users import get_user_by_id
from caringapp.endpoints.users.schemas import user_display_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('users', __name__)


@blueprint.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    response = user_display_schema.dump(user)

    return jsonify(response)
