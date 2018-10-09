import uuid

from datetime import datetime
from core import configuration, errors
from core.aws.cognito import create_user, generate_random_password
from core.aws.ses import SES
from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs
from .model import OrganizationModel
from .resource import organization_details_schema, organization_schema, organization_verification_schema

import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('organizations', __name__)


@blueprint.route('/register-organization', methods=["POST"])
@use_kwargs(organization_details_schema, locations=('json',))
def add_organization(**kwargs):
    # TODO: Enhance duplicate check to use Global Secondary Indexes, decorators, and updated rules (name, address, etc.)
    name = kwargs['name']
    if len(list(OrganizationModel.scan(OrganizationModel.name == name))) > 0:
        message = 'Organization with name {} already exists'.format(name)
        raise errors.ResourceValidationError(messages={'name': [message]})

    organization = OrganizationModel(id=str(uuid.uuid4()),
                                     name=name,
                                     description=kwargs['description'],
                                     contact_details=kwargs['contact_details'])

    organization.save()

    # Send an email to the administrator for verification
    recipients = [configuration.get_setting('verification_email_recipient')]
    try:
        ses = SES()
        # TODO: Format email message
        ses.send_email(recipients=recipients,
                       subject='New Organization Request',
                       body='New organization request for {}.  Please go to {} to verify the request.'.format(
                           name,
                           'https://dev-api.caringcalendar.com/verify'
                       ))
    except errors.SESError:
        # TODO: In addition to logging message include in response message indicating that the email failed to send
        logger.warning('Organization {} created; error sending email to {}.'.format(name, recipients))

    response = jsonify(organization_details_schema.dump(organization).data)
    response.status_code = 201

    return response


@blueprint.route('/organizations', methods=["GET"])
def list_organizations():
    organizations = OrganizationModel.scan()
    response = []

    for org in organizations:
        response.append(organization_schema.dump(org).data)

    return jsonify(response)


@blueprint.route('/organizations/<org_id>', methods=["GET"])
def retrieve_organization(org_id):
    organization = get_organization_from_db(org_id)
    return jsonify(organization_details_schema.dump(organization).data)


@blueprint.route('/organizations/<org_id>/verify', methods=["POST"])
@use_kwargs(organization_verification_schema, locations=('json',))
def verify_organization(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    is_verified = kwargs['is_verified']

    if is_verified and not organization.is_verified:
        # Update the verification flag
        organization.update(
            actions=[
                OrganizationModel.is_verified.set(is_verified),
                OrganizationModel.updated.set(datetime.now())
            ]
        )

        # Create the Cognito user for organization's contact
        contact_details = organization.contact_details
        if contact_details:
            username = contact_details['email']
            password = generate_random_password()
            create_user(username, password)

        # TODO: Create the user record in the database

    response = jsonify(organization_details_schema.dump(organization).data)
    response.status_code = 201
    return response

@blueprint.route('/organizations/<org_id>/', methods=["PUT"])
@use_kwargs(organization_schema, locations=('json',))
def update_organization(org_id, **kwargs):
    organization = get_organization_from_db(org_id)
    name = kwargs['name'] # if( kwargs['name'] is not None and len(kwargs['name']) > 0) else organization.name
    description = kwargs['description'] 
    if organization.name != name :
        if len(list(OrganizationModel.scan(OrganizationModel.name == name))) > 0:
            message = 'Organization with name {} already exists'.format(name)
            raise errors.ResourceValidationError(messages={'name': [message]})
    # contact_details = kwargs['contact_details'] if( kwargs['contact_details'] is not None and len(kwargs['contact_details']) > 0) else organization.contact_details
    
    organization.update(
        actions=[
            OrganizationModel.name.set(name),
            OrganizationModel.description.set(description),
            # OrganizationModel.contact_details.set(contact_details),
            OrganizationModel.updated.set(datetime.now())
        ]
    )
    return jsonify(organization_details_schema.dump(organization).data)
        
def get_organization_from_db(org_id):
    try:
        return OrganizationModel.get(hash_key=org_id)
    except OrganizationModel.DoesNotExist:
        message = 'Organization {} does not exist'.format(org_id)
        raise errors.ResourceValidationError(messages={'name': [message]})