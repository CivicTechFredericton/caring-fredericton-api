from core import configuration, db, errors
from core.aws.ses import SES
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.users import create_user
from core.db.users.model import UserModel

from services.users import build_filter_condition
from services.users.resource import user_registration_schema, user_display_schema, user_list_filter_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('users', __name__)


@blueprint.route('/users/register', methods=["POST"])
@use_kwargs(user_registration_schema, locations=('json',))
def register_user(**kwargs):

    # create user entries in db and cognito 
    user = create_user(kwargs)

    # print a nice response (leave out password) 
    response = jsonify(user_registration_schema.dump(user).data)
    response.status_code = 201

    return response


@blueprint.route('/users', methods=["GET"])
@use_kwargs(user_list_filter_schema, locations=('query',))
def list_users(**kwargs):
    filter_condition = build_filter_condition(**kwargs)
    users = UserModel.scan(filter_condition)

    response = []

    for user in users:
        response.append(user_display_schema.dump(user).data)

    return jsonify(response)

