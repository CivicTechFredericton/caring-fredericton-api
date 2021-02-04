from caringapp.core.errors import ResourceNotFoundError, ResourceConflictError
from caringapp.db.users.model import UserModel


def get_user_by_id(user_id):
    try:
        return UserModel.get(hash_key=user_id)
    except UserModel.DoesNotExist:
        message = 'User {} does not exist'.format(user_id)
        raise ResourceNotFoundError(messages={'name': [message]})


def check_user_exists(email):
    count = UserModel.user_email_index.count(hash_key=email)

    if count > 0:
        message = f"User with address {email} already created"
        raise ResourceConflictError(messages={'email': [message]})


def get_user_by_email(email):
    user_list = UserModel.user_email_index.query(hash_key=email)
    user = next(user_list, None)

    if user is None:
        raise ResourceNotFoundError

    return user
