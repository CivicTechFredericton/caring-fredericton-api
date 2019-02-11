from core import errors
from core.db.users.model import UserModel 

from core.aws.cognito import create_cognito_user, generate_random_password 

# TODO: Enhance duplicate check to use Global Secondary Indexes, decorators, and updated rules (name, address, etc.)
def check_for_duplicate_user(user_email):
    if len(list(UserModel.scan(UserModel.email == user_email))) > 0:
        message = 'User with name {} already exists'.format(user_email)
        raise errors.ResourceValidationError(messages={'email': [message]})

# create cognito and user db entries for a given user from a dictionary
# email, password, first_name, last_name are required fields 
# returns a persisted UserModel
def create_user(user_args):

	# check for duplicates using the email as a public unique ID
    email = user_args['email']
    check_for_duplicate_user(email)
	
    # Create the Cognito user for organization's administrator
    # TODO: add password strength checks if neeed
    password = user_args['password'] 
    create_cognito_user(email, password)

    # Create the user model (remove the password from the input args since we don't 
    # store it in DynamoDB)
    user_args.pop('password')

    user = UserModel(user_args)
    db.save_with_unique_id(user)

    return user	
