import boto3
import math
import random
import os
import string

from core import configuration
from core.errors import CognitoError

import logging
logger = logging.getLogger(__name__)

ADMIN_CREATE_USER = 'admin_create_user'
ADMIN_GET_USER = 'admin_get_user'
DESCRIBE_USER_POOL = 'describe_user_pool'


def open_cognito_connection():
    return boto3.client('cognito-idp')


def send_cognito_command(command, arguments=None):
    logger.debug("Sending Cognito command '%s'" % command,
                 extra={'arguments': arguments})

    if arguments is None:
        arguments = {}

    client = open_cognito_connection()
    try:
        # TODO: Set the envrionment variable when using 'local' option
        # user_pool_id = os.environ['COGNITO_USER_POOL_USERS_ID']
        user_pool_id = get_user_pool_id(client)
        response = getattr(client, command)(
            UserPoolId=user_pool_id,
            **arguments
        )
    except Exception as e:
        logger.error("Error sending command to cognito: %s" % str(e))
        raise CognitoError()

    return response


def get_user_pool_id(cognito_idp_client):
    # Find the details of the user pool
    service_name = configuration.get_setting('SERVICE_NAME')
    stage = configuration.get_setting('STAGE')
    user_pool_name = '{}-{}-users'.format(service_name, stage)

    response = cognito_idp_client.list_user_pools(
        MaxResults=60
    )

    for user_pool in response['UserPools']:
        if user_pool['Name'] == user_pool_name:
            user_pool_id = user_pool['Id']
            break

    return user_pool_id

# def get_userpool_passwordpolicy():
#     pool_details = send_cognito_command(DESCRIBE_USER_POOL)
#     return pool_details['UserPool']['Policies']['PasswordPolicy']
#
#
# def describe_user_pool():
#     return send_cognito_command('describe_user_pool')


def generate_random_password():
    # Using the password policy rules generate a random password
    pool_details = send_cognito_command(DESCRIBE_USER_POOL)
    password_policy = pool_details['UserPool']['Policies']['PasswordPolicy']

    min_length = password_policy.get('MinimumLength')
    require_uppercase = password_policy.get('RequireUppercase')
    require_lowercase = password_policy.get('RequireLowercase')
    require_numbers = password_policy.get('RequireNumbers')
    require_symbols = password_policy.get('RequireSymbols')

    chars = string.ascii_lowercase
    new_pass = ''.join(random.choice(chars) for x in range(min_length))

    if require_uppercase:
        index = int(math.ceil(min_length * .2))
        uppers = ''.join(random.choice(string.ascii_uppercase) for x in range(2))
        new_pass = new_pass[:index] + uppers + new_pass[index + 2:]

    if require_numbers:
        index = int(math.ceil(min_length * .5))
        numbers = ''.join(random.choice(string.digits) for x in range(2))
        new_pass = new_pass[:index] + numbers + new_pass[index + 2:]
    if require_numbers:
        chars += string.digits

    if require_symbols:
        index = int(math.ceil(min_length * .8))
        numbers = ''.join(random.choice(string.punctuation) for x in range(2))
        new_pass = new_pass[:index] + numbers + new_pass[index + 2:]

    if require_lowercase:
        lower_flag = any(c.islower() for c in new_pass)

        if not lower_flag:
            lower_char = ''.join(random.choice(string.ascii_lowercase) for x in range(1))
            new_pass = lower_char + new_pass[1:]

    lst_pass = list(new_pass)
    random.shuffle(lst_pass)
    new_pass = ''.join(lst_pass)
    return new_pass


def create_user(username, password, suppress=False):
    user = send_cognito_command(ADMIN_GET_USER,
                                arguments={'Username': username})

    if not user:
        args = {
            'Username': username,
            'TemporaryPassword': password
            # 'UserAttributes': [
            #     {
            #         'Name': 'email',
            #         'Value': username
            #     },
            #     {
            #         'Name': 'email_verified',
            #         'Value': 'True'
            #     },
            # ]
        }

        if suppress:
            args['MessageAction'] = 'SUPPRESS'

        result = send_cognito_command(ADMIN_CREATE_USER, arguments=args)

    return result['User']
