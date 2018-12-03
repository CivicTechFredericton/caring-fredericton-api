from core import errors
from core.db.organizations.model import OrganizationModel


def check_for_duplicate_name(org_name):
    if len(list(OrganizationModel.scan(OrganizationModel.name == org_name))) > 0:
        message = 'Organization with name {} already exists'.format(org_name)
        raise errors.ResourceValidationError(messages={'name': [message]})


def get_organization_from_db(org_id):
    try:
        return OrganizationModel.get(hash_key=org_id)
    except OrganizationModel.DoesNotExist:
        message = 'Organization {} does not exist'.format(org_id)
        raise errors.ResourceValidationError(messages={'name': [message]})
