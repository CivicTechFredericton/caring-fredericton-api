import json
import uuid

from flask import Blueprint, jsonify
from webargs.flaskparser import use_kwargs
from .model import OrganizationModel
from .resource import organization_schema

blueprint = Blueprint('organizations', __name__)


@blueprint.route('/organizations', methods=["GET"])
def list_organizations():
    organizations = OrganizationModel.scan()
    response = []

    for org in organizations:
        response.append(organization_schema.dump(org).data)

    return jsonify(response)


@blueprint.route('/organizations/registration', methods=["POST"])
@use_kwargs(organization_schema, locations=('json',))
def add_organization(**kwargs):
    # TODO: Add duplicate organization check (name, address - define rules)
    organization = OrganizationModel(id=str(uuid.uuid4()),
                                     name=kwargs['name'],
                                     description=kwargs['description'],
                                     is_verified=False)

    organization.save()

    response = jsonify(organization_schema.dump(organization).data)
    response.status_code = 201

    return response


@blueprint.route('/organizations/<org_id>/verify', methods=["PUT"])
def verify_organization(org_id):
    try:
        # TODO: Create the user record in Cognito and the database

        # Update the verification flag and assign the user to the organization
        organization = OrganizationModel.get(hash_key=org_id)
        organization.update(
            actions=[
                OrganizationModel.is_verified.set(True)
            ]
        )

        response = jsonify(organization_schema.dump(organization).data)
        response.status_code = 201

    except OrganizationModel.DoesNotExist:
        response = jsonify({'message': 'Organization {} does not exist'.format(org_id)})
        response.status_code = 422

    return response
