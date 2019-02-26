from core import errors
from core.db.users.model import UserModel 
from core import db 

from core.aws.cognito import create_cognito_user, generate_random_password 

# get a user by email
def get_user_by_email(user_email):
    users = list(UserModel.scan(UserModel.email == user_email))
    
    if(users == []):
        message = 'User with email {} does not exist'.format(user_email)
        raise errors.ResourceValidationError(messages={'email': [message]})

    if(len(users) ):
        message = 'More than one user with email {}'.format(user_email)
        raise errors.ResourceValidationError(messages={'email': [message]})

	# convert from list to single instance
    return users[0]

def get_user_by_id(user_id):
    users = list(UserModel.scan(UserModel.id == user_id))

    if(users == []):
        message = 'User with id {} does not exist'.format(user_id)
        raise errors.ResourceValidationError(messages={'id': [message]})

    if(len(users)>1 ):
        message = 'More than one user with id {}'.format(user_id)
        raise errors.ResourceValidationError(messages={'id': [message]})

    return user[0]
  
# TODO: Enhance duplicate check to use Global Secondary Indexes, decorators, and updated rules (name, address, etc.)
def check_duplicate_user_email(user_email):
    if len(list(UserModel.scan(UserModel.email == user_email))) > 0:
        message = 'User with email {} already exists'.format(user_email)
        raise errors.ResourceValidationError(messages={'email': [message]})

# create cognito and user db entries for a given user from a dictionary
# email, password, first_name, last_name are required fields 
# returns a persisted UserModel
def create_user(**user_args):

	# check for duplicates using the email as a public unique ID
    email = user_args['email']
    check_duplicate_user_email(email)
	
    # Create the Cognito user for organization's administrator
    # TODO: add password strength checks if needed
    password = user_args['password']
    # password = generate_random_password() 
    create_cognito_user(email, password)

    # Create the user model (remove the password from the input args since we don't 
    # store it in DynamoDB)
    user_args.pop('password')

    user = UserModel(**user_args)
    db.save_with_unique_id(user)

    return user	
