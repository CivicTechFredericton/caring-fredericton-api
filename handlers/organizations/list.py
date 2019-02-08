import json

from core.db.organizations import OrganizationModel
from handlers.api_utils import set_dynamo_table_name
from handlers.organizations import organization_list_schema


def handler(event, context):
    """
    List the registered organizations
    :return: The list of events in the system
    """
    set_dynamo_table_name(OrganizationModel)

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
