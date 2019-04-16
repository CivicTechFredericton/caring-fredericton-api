from core.aws.cognito import create_user
from core.db import save_with_unique_id
from core.db.users.model import UserModel
from core.errors import ResourceConflictError


def create_new_user(**kwargs):
    email = kwargs.get('email')

    try:
        create_user(email, kwargs.get('password'))

        user = UserModel(**kwargs)
        save_with_unique_id(user)

        return user
    except Exception as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            message = f"User with name {email} already created"
            raise ResourceConflictError(messages={'folderName': [message]})

# get a user by email
# def get_user_by_email(user_email):
#     users = list(UserModel.scan(UserModel.email == user_email))
#
#     if(users == []):
#         message = 'User with email {} does not exist'.format(user_email)
#         raise ResourceValidationError(messages={'email': [message]})
#
#     if(len(users)>1):
#         message = 'More than one user with email {}'.format(user_email)
#         raise ResourceValidationError(messages={'email': [message]})
#
# 	# convert from list to single instance
#     return users[0]


# def get_user_by_id(user_id):
#     users = list(UserModel.scan(UserModel.id == user_id))
#
#     if(users == []):
#         message = 'User with id {} does not exist'.format(user_id)
#         raise ResourceValidationError(messages={'id': [message]})
#
#     if(len(users)>1 ):
#         message = 'More than one user with id {}'.format(user_id)
#         raise ResourceValidationError(messages={'id': [message]})
#
#     return users[0]
