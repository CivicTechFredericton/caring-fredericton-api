from core.db import get_filter_conditions
from core.db.organizations import check_for_duplicate_name
from core.db.organizations.model import OrganizationModel
from core.utils import retrieve_value_from_args


def build_filter_condition(**kwargs):
    conditions = []

    is_verified = retrieve_value_from_args('is_verified', kwargs)
    if is_verified is not None:
        conditions.append(OrganizationModel.is_verified == is_verified)

    return get_filter_conditions(conditions)


def build_verify_organization_actions(is_verified):
    return [OrganizationModel.is_verified.set(is_verified)]


def build_update_actions(organization, **kwargs):
    actions = []

    name = retrieve_value_from_args('name', kwargs)
    if name and name != organization.name:
        check_for_duplicate_name(name)
        actions.append(OrganizationModel.name.set(name))

    email = retrieve_value_from_args('email', kwargs)
    if email and email != organization.email:
        actions.append(OrganizationModel.email.set(email))

    phone = retrieve_value_from_args('phone', kwargs)
    if phone and phone != organization.phone:
        actions.append(OrganizationModel.phone.set(phone))

    address = retrieve_value_from_args('address', kwargs)
    if address and address != organization.address:
        actions.append(OrganizationModel.address.set(address))

    return actions
