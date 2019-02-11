from core import configuration, db, errors
from core.aws.cognito import create_user, generate_random_password
from core.aws.ses import SES
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.users import check_for_duplicate_user
from core.db.users.model import UserModel

from services.users import build_filter_condition
from services.users.resource import user_schema, user_list_filter_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('users', __name__)


@blueprint.route('/register-user', methods=["POST"])
@use_kwargs(user_schema, locations=('json',))
def register_user(**kwargs):
    # TODO: Enhance duplicate check to use Global Secondary Indexes, decorators, and updated rules (name, address, etc.)
    email = kwargs['email']
    check_for_duplicate_user(email)

    user = UserModel(**kwargs)
    #db.save_with_unique_id(user)

    response = jsonify(user_schema.dump(user).data)
    response.status_code = 201

    return response


@blueprint.route('/users', methods=["GET"])
@use_kwargs(user_list_filter_schema, locations=('query',))
def list_users(**kwargs):
    filter_condition = build_filter_condition(**kwargs)
    users = UserModel.scan(filter_condition)

    response = []

    for user in users:
        response.append(user_schema.dump(user).data)

    return jsonify(response)

