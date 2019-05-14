from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.aws.cognito import create_user
from core.db import save_item
from core.db.users import get_user_by_id
from core.db.users.model import UserModel
from core.errors import ResourceConflictError, BadRequestError

from services.users.resource import user_registration_schema, user_display_schema


import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('users', __name__)


@blueprint.route('/users/signup', methods=["POST"])
@use_kwargs(user_registration_schema, locations=('json',))
def create_new_user(**kwargs):
    user_args = {k: v for k, v in kwargs.items() if v is not None}

    email = user_args.get('email')

    try:
        cognito_response = create_user(email, kwargs.get('password'))
        user_args['id'] = cognito_response['UserSub']
    except Exception as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            message = f"User with name {email} already created"
            raise ResourceConflictError(messages={'email': [message]})
        else:
            message = 'Error occurred when creating user'
            raise BadRequestError(messages={'email': [message]})

    user = UserModel(id=user_args['id'],
                     email=email,
                     first_name=kwargs.get('first_name'),
                     last_name=kwargs.get('last_name'))
    save_item(user)

    response = jsonify(user_display_schema.dump(user).data)
    response.status_code = 201

    return response


@blueprint.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    response = user_display_schema.dump(user).data

    return jsonify(response)


# @blueprint.route('/users/<user_id>/join/<org_id>', methods=["POST"])
# @use_kwargs(user_join_org_schema, locations=('json',))
# def join_org(user_id, org_id):
#     # Check user existence
#     user = get_user_by_id(user_id)
#
#     # Check organization existence
#     org = get_organization_from_db(org_id)
#
#     # Update the user's organization ID
#     actions = [UserModel.organization_id.set(org.id)]
#     update_item(user, actions)
#
#     response = jsonify(user_display_schema.dump(user).data)
#     response.status_code = 201
#
#     return response
