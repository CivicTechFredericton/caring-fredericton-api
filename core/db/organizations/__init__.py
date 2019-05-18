from core.db.organizations.model import OrganizationModel
from core.errors import ResourceConflictError, ResourceNotFoundError, ResourceValidationError


def check_for_duplicate_name(name):
    count = OrganizationModel.search_name.count(hash_key=name.lower())

    if count > 0:
        message = 'Organization with name {} already exists'.format(name)
        raise ResourceConflictError(messages={'name': [message]})


def get_organization_from_db(org_id):
    try:
        return OrganizationModel.get(hash_key=org_id)
    except OrganizationModel.DoesNotExist:
        message = 'Organization {} does not exist'.format(org_id)
        raise ResourceNotFoundError(messages={'name': [message]})


def get_verified_organization_from_db(org_id):
    """
    Returns a valid organization from db, raise exception if it doesn't exist
    :param org_id:
    :return:
    """
    organization = get_organization_from_db(org_id)

    if organization.is_verified:
        return organization
    else:
        message = 'Organization {} has not been verified'.format(org_id)
        raise ResourceValidationError(messages={'name': [message]})
