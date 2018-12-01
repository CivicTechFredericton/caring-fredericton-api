from core.db import get_filter_conditions
from core.db.organizations import check_for_duplicate_name
from core.db.organizations.model import OrganizationModel
from webargs import missing


def build_filter_condition(**kwargs):
    conditions = []

    is_verified = kwargs['is_verified']
    if is_verified is not missing:
        conditions.append(OrganizationModel.is_verified == is_verified)

    return get_filter_conditions(conditions)


def build_verify_organization_actions(is_verified):
    return [OrganizationModel.is_verified.set(is_verified)]


def build_update_actions(organization, **kwargs):
    actions = []

    name = kwargs['name']
    if name and name != organization.name:
        check_for_duplicate_name(name)
        actions.append(OrganizationModel.name.set(name))

    email = kwargs['email']
    if email and email != organization.email:
        actions.append(OrganizationModel.email.set(email))

    phone = kwargs['phone']
    if phone and phone != organization.phone:
        actions.append(OrganizationModel.phone.set(phone))

    address = kwargs['address']
    if address and address != organization.address:
        actions.append(OrganizationModel.address.set(address))

    return actions
