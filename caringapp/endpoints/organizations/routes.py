from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from caringapp import db
from caringapp.aws.ses import send_email
from caringapp.core import configuration, errors
from caringapp.core.request import generate_web_url
from caringapp.db.organizations import check_for_duplicate_name, get_organization_from_db
from caringapp.db.organizations.model import OrganizationModel
from caringapp.db.users import get_user_by_id

from caringapp.endpoints.organizations import build_verify_organization_actions, build_user_organization_actions, \
    build_scan_condition, build_update_actions
from caringapp.endpoints.organizations.schemas import organization_details_schema, organization_verification_schema, \
    organization_list_filters_schema, organization_schema, organization_update_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('organizations', __name__)


# ----------------------------------
# Organization Registration Routes
# ----------------------------------
# @blueprint.route('/guests/organizations', methods=["GET"])
# def list_verified_organizations():
#     organizations = OrganizationModel.scan(OrganizationModel.is_verified == True)
#     response = [organization_list_schema.dump(org) for org in organizations]
#
#     return jsonify(response)

# ----------------------------------
# Organization Registration Routes
# ----------------------------------
@blueprint.route('/organizations', methods=["POST"])
@use_kwargs(organization_details_schema, location='json')
def create_organization(**kwargs):
    name = kwargs['name']
    check_for_duplicate_name(name)

    # Verify the that administrator user exists in the system
    get_user_by_id(kwargs['administrator_id'])

    # Create the organization
    organization = OrganizationModel(**kwargs)
    db.save_with_unique_id(organization)

    # Send an email to the administrator for verification
    recipients = [configuration.get_setting('ORG_VERIFICATION_EMAIL_RECIPIENT')]
    try:
        verification_url = generate_web_url(f"/validation/{organization.id}")
        send_email(recipients=recipients,
                   subject='New Organization Request',
                   text_body='New Caring Calendar organization request for {}.  '
                             'Please go to {} to verify the request.'.format(name, verification_url))
    except errors.SESError:
        # TODO: In addition to logging message include in response message indicating that the email failed to send
        logger.warning('Organization {} created; error sending email to {}.'.format(name, recipients))

    response = jsonify(organization_details_schema.dump(organization))
    response.status_code = 201

    return response


@blueprint.route('/organizations/<org_id>/verify', methods=["POST"])
@use_kwargs(organization_verification_schema, location='json')
def verify_organization(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    is_verified = kwargs['is_verified']

    if is_verified and not organization.is_verified:
        organization_actions = build_verify_organization_actions(is_verified)
        db.update_item(organization, organization_actions)

        # we've verified the organization and ensured that the admin user
        # is a valid user so add the organization to
        org_user = get_user_by_id(organization.administrator_id)
        user_actions = build_user_organization_actions(organization)
        db.update_item(org_user, user_actions)

        recipient = org_user.email
        try:
            # Send the user an email indicating the organization has been verified
            signin_url = generate_web_url("/signin")
            send_email(recipients=[recipient],
                       subject='Organization Request Approved',
                       text_body='The organization {} has been approved for use in the Caring Calendar.  '
                                 'Please go to {} to start entering events.'.format(
                               organization.name,
                               signin_url
                           ))
        except errors.SESError:
            logger.warning(f"Error sending email to {recipient}")

    return jsonify(organization_details_schema.dump(organization))


# ----------------------------------
# Organization Management Routes
# ----------------------------------
@blueprint.route('/organizations', methods=["GET"])
@use_kwargs(organization_list_filters_schema, location='query')
def list_organizations(**kwargs):
    scan_condition = build_scan_condition(**kwargs)
    organizations = OrganizationModel.scan(scan_condition)

    response = [organization_schema.dump(org) for org in organizations]
    return jsonify(response)


@blueprint.route('/organizations/<org_id>', methods=["GET"])
def retrieve_organization(org_id):
    organization = get_organization_from_db(org_id)
    admin_user = get_user_by_id(organization.administrator_id)
    organization.administrator_details = {
        'email': admin_user.email,
        'first_name': admin_user.first_name,
        'last_name': admin_user.last_name
    }
    return jsonify(organization_details_schema.dump(organization))


@blueprint.route('/organizations/<org_id>', methods=["PUT"])
@use_kwargs(organization_update_schema, location='json')
def update_organization(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    actions = build_update_actions(organization, **kwargs)
    db.update_item(organization, actions)

    return jsonify(organization_details_schema.dump(organization))
