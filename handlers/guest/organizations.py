import json
import os

from core.db.organizations import OrganizationModel
from services.public.resource import organization_list_schema


def handler(event, context):
    """
    List the registered organizations
    :return: The list of events in the system
    """
    service_name = os.environ['SERVICE_NAME']
    stage_name = os.environ['STAGE']
    OrganizationModel.Meta.table_name = \
        '{}-{}-{}'.format(service_name, stage_name, OrganizationModel.Meta.simple_name)

    organizations = OrganizationModel.scan(OrganizationModel.is_verified == True)
    response_list = [organization_list_schema.dump(org).data for org in organizations]

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps({'items': response_list})
    }
