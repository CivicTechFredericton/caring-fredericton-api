from core.db.users.model import UserModel
from core.errors import ResourceConflictError, ResourceNotFoundError


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
    user = UserModel.user_email_index.query(hash_key=email)

    return user
