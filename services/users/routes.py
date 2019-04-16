from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.aws.cognito import create_user
from core.db import save_with_unique_id
from core.db.users.model import UserModel
from core.errors import ResourceConflictError

from services.organizations import build_scan_condition
from services.users.resource import user_registration_schema, user_display_schema, user_join_org_schema

from core.db.organizations import get_organization_from_db 


import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('users', __name__)


@blueprint.route('/users/signup', methods=["POST"])
@use_kwargs(user_registration_schema, locations=('json',))
def create_new_user(**kwargs):
    try:
        email = kwargs.get('email')
        create_user(email, kwargs.get('password'))
    except Exception as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            message = f"User with name {email} already created"
            raise ResourceConflictError(messages={'folderName': [message]})

    user = UserModel(**kwargs)
    save_with_unique_id(user)

    response = jsonify(user_display_schema.dump(user).data)
    response.status_code = 201

    return response


# def register_user(**kwargs):
#     user = create_new_user(**kwargs)
#
#     response = jsonify(user_display_schema.dump(user).data)
#     response.status_code = 201
#     return response
#
#     # try:
#     #     # Check for duplicate email address
#     #     # email = kwargs.get('email')
#     #     # check_duplicate_user_email(email)
#     #
#     #     cognito.create_user(kwargs.get('email'), kwargs.get('password'))
#     #
#     #     user = create_user(**kwargs)
#     #
#     #     response = jsonify(user_display_schema.dump(user).data)
#     #     response.status_code = 201
#     #     return response
#     # except Exception as e:
#     #     if e.response['Error']['Code'] == 'UsernameExistsException':
#     #         message = f"User with name {email} already created"
#     #         raise ResourceConflictError(messages={'folderName': [message]})
#     #         response = response_template(400)
#     #         response['body'] = json.dumps({
#     #             'error_message': f"User with name {email} already created"
#     #         })
#     #
#     #         return response
#
#     # create user entries in db and cognito
#     # user = create_user(**kwargs)
#     #
#     # # print a nice response (leave out password)
#     # response = jsonify(user_display_schema.dump(user).data)
#     # response.status_code = 201
#     #
#     # return response


# @blueprint.route('/users', methods=["GET"])
# @use_kwargs(user_list_filter_schema, locations=('query',))
# def list_users(**kwargs):
#     filter_condition = build_scan_condition(**kwargs)
#     users = UserModel.scan(filter_condition)
#
#     response = []
#
#     for user in users:
#         response.append(user_display_schema.dump(user).data)
#
#     return jsonify(response)


@blueprint.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id) 
    response = user_display_schema.dump(user).data

    return jsonify(response)


# @blueprint.route('/users/activate', methods=["POST"])
# @use_kwargs(user_activation_schema, locations=('json',))
# def activate_user(**kwargs):
#
#     # look the user up by email (raises if the user isn't found)
#     email = kwargs['email']
#     user = get_user_by_email(email)
#
#     # run through the first login password change (raises if there's a problem)
#     old_password = kwargs['password']
#     new_password = kwargs['new_password']
#     result = manage_first_login(email, old_password, new_password)
#
#     # set user active
#     user.active = True
#     user.save()
#
#     # send back the access token (user is logged in)
#     token = {
#         'authToken': result['AccessToken']
#     }
#     response = jsonify(token)
#     response.status_code = 201
#
#     return response


@blueprint.route('/users/<user_id>/join/<org_id>', methods=["POST"])
@use_kwargs(user_join_org_schema, locations=('json',))
def join_org(user_id, org_id, **kwargs):

    # get the user (check to see if they exist) 
    user = get_user_by_id(user_id)
   
    # get the organization (check to see if it exists)
    org = get_organization_from_db(org_id) 

    # set the id and save
    user.organization_id = org_id
    user.save()

    # print a nice response (leave out password) 
    response = jsonify(user_display_schema.dump(user).data)
    response.status_code = 201

    return response
