from core import errors
from core.db.users.model import UserModel 

def check_for_duplicate_user(user_email):
    if len(list(UserModel.scan(UserModel.email == user_email))) > 0:
        message = 'User with name {} already exists'.format(user_email)
        raise errors.ResourceValidationError(messages={'email': [message]})

