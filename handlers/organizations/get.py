from core.db.organizations.model import OrganizationModel
from core.db.organizations import get_organization_from_db
from services.organizations.resource import organization_details_schema
from handlers.api_utils import set_dynamo_table_name


def handler(event, context):
    set_dynamo_table_name(OrganizationModel)

    org_id = event['path']['org_id']
    organization = get_organization_from_db(org_id)

    return organization_details_schema.dump(organization).data
