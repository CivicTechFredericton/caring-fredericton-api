from core import configuration, db, errors
from core.aws.cognito import manage_first_login
from core.aws.ses import SES
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.users import create_user, get_user_by_id, get_user_by_email
from core.db.users.model import UserModel

from services.organizations import build_scan_condition
from services.users.resource import user_registration_schema, user_display_schema, user_list_filter_schema,user_activation_schema 

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('users', __name__)


@blueprint.route('/users/register', methods=["POST"])
@use_kwargs(user_registration_schema, locations=('json',))
def register_user(**kwargs):

    # create user entries in db and cognito 
    user = create_user(**kwargs)

    # print a nice response (leave out password) 
    response = jsonify(user_display_schema.dump(user).data)
    response.status_code = 201

    return response


@blueprint.route('/users', methods=["GET"])
@use_kwargs(user_list_filter_schema, locations=('query',))
def list_users(**kwargs):
    filter_condition = build_scan_condition(**kwargs)
    users = UserModel.scan(filter_condition)

    response = []

    for user in users:
        response.append(user_display_schema.dump(user).data)

    return jsonify(response)


@blueprint.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id) 

    response = user_display_schema.dump(user).data

    return jsonify(response)

@blueprint.route('/users/activate', methods=["POST"])
@use_kwargs(user_activation_schema, locations=('json',))
def activate_user(**kwargs):

    # look the user up by email (raises if the user isn't found)
    email = kwargs['email']
    user = get_user_by_email(email)

    # run through the first login password change (raises if there's a problem) 
    old_password = kwargs['password']
    new_password = kwargs['new_password']
    result = manage_first_login(email, old_password, new_password)

    # set user active
    user.active = True 
    user.save()

    # send back the access token (user is logged in) 
    token = {
        'authToken': result['AccessToken']
    }
    response = jsonify(token)
    response.status_code = 201

    return response

