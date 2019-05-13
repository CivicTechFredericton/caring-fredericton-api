from core import configuration, db, errors
from core.aws.ses import SES
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs

from core.db.organizations import check_for_duplicate_name, get_organization_from_db
from core.db.organizations.model import OrganizationModel
from core.db.users import get_user_by_email, get_user_by_id

from services.organizations import build_scan_condition, build_update_actions, build_verify_organization_actions
from services.organizations.resource import organization_details_schema, organization_list_filters_schema,\
    organization_schema, organization_update_schema, organization_verification_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('organizations', __name__)


# ----------------------------------
# Organization Registration Routes
# ----------------------------------
@blueprint.route('/organizations/register', methods=["POST"])
@use_kwargs(organization_details_schema, locations=('json',))
def register_organization(**kwargs):
    name = kwargs['name']
    check_for_duplicate_name(name)

    # Verify the that administrator user exists in the system
    admin_email = kwargs['administrator_email']
    admin_user = get_user_by_email(admin_email)

    # Set the administrator id to the admin users's email
    # The org will be added to the admin user's account when verified
    kwargs['administrator_id'] = admin_user.id

    # Create the organization
    organization = OrganizationModel(**kwargs)
    db.save_with_unique_id(organization)

    # Send an email to the administrator for verification
    recipients = [configuration.get_setting('verification_email_recipient')]
    try:
        ses = SES()
        # TODO: Format email message
        verification_url = f"{configuration.get_setting('UI_DOMAIN_NAME')}/validation/{organization.id}"
        ses.send_email(recipients=recipients,
                       subject='New Organization Request',
                       body='New organization request for {}.  Please go to {} to verify the request.'.format(
                           name,
                           verification_url
                       ))
    except errors.SESError:
        # TODO: In addition to logging message include in response message indicating that the email failed to send
        logger.warning('Organization {} created; error sending email to {}.'.format(name, recipients))

    response = jsonify(organization_details_schema.dump(organization).data)
    response.status_code = 201

    return response


@blueprint.route('/organizations/<org_id>/verify', methods=["POST"])
@use_kwargs(organization_verification_schema, locations=('json',))
def verify_organization(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    is_verified = kwargs['is_verified']

    if is_verified and not organization.is_verified:
        actions = build_verify_organization_actions(is_verified)
        db.update_item(organization, actions)

        # we've verified the organization and ensured that the admin user
        # is a valid user so add the organization to
        admin = get_user_by_id(organization.administrator_id)
        admin.organization_id = organization.id
        admin.save()

    return jsonify(organization_details_schema.dump(organization).data)


# ----------------------------------
# Organization Management Routes
# ----------------------------------
@blueprint.route('/organizations', methods=["GET"])
@use_kwargs(organization_list_filters_schema, locations=('query',))
def list_organizations(**kwargs):
    scan_condition = build_scan_condition(**kwargs)
    organizations = OrganizationModel.scan(scan_condition)

    response = [organization_schema.dump(org).data for org in organizations]
    return jsonify(response)


@blueprint.route('/organizations/<org_id>', methods=["GET"])
def retrieve_organization(org_id):
    organization = get_organization_from_db(org_id)
    return jsonify(organization_details_schema.dump(organization).data)


@blueprint.route('/organizations/<org_id>', methods=["PUT"])
@use_kwargs(organization_update_schema, locations=('json',))
def update_organization(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    actions = build_update_actions(organization, **kwargs)
    db.update_item(organization, actions)

    return jsonify(organization_details_schema.dump(organization).data)
