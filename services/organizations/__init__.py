from core.db import get_filter_conditions
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


def build_update_actions(**kwargs):
    actions = []

    name = kwargs['name']
    if name:
        actions.append(OrganizationModel.name.set(name))

    email = kwargs['email']
    if email:
        actions.append(OrganizationModel.email.set(email))

    phone = kwargs['phone']
    if phone:
        actions.append(OrganizationModel.phone.set(phone))

    address = kwargs['address']
    if address:
        actions.append(OrganizationModel.address.set(address))

    return actions


def set_attribute_update(name, value):
    return f'OrganizationModel.{name}.set({value})'
