from core import configuration, db, errors
from core.aws.cognito import create_user, generate_random_password
from core.aws.ses import SES
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.organizations import check_for_duplicate_name, get_organization_from_db
from core.db.organizations.model import OrganizationModel
from core.db.users.model import UserModel
from services.organizations import build_filter_condition, build_update_actions, build_verify_organization_actions
from services.organizations.resource import organization_details_schema, organization_list_filters_schema,\
    organization_schema, organization_update_schema, organization_verification_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('organizations', __name__)


@blueprint.route('/register-user', methods=["POST"])
@use_kwargs(user_schema, locations=('json',))
def register_user(**kwargs):
    # TODO: Enhance duplicate check to use Global Secondary Indexes, decorators, and updated rules (name, address, etc.)
    username = kwargs['username']
    check_for_duplicate_name(username)

    user = UserModel(**kwargs)
    #db.save_with_unique_id(user)

    response = jsonify(user_schema.dump(user).data)
    response.status_code = 201

    return response


@blueprint.route('/users', methods=["GET"])
@use_kwargs(organization_list_filters_schema, locations=('query',))
def list_users(**kwargs):
    filter_condition = build_filter_condition(**kwargs)
    users = UserModel.scan(filter_condition)

    response = []

    for user in users:
        response.append(user_schema.dump(org).data)

    return jsonify(response)

