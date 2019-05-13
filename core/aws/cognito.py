import boto3
from botocore.errorfactory import ClientError
from core.configuration import get_setting

import logging
logger = logging.getLogger(__name__)

SIGN_UP = 'sign_up'


def open_cognito_connection():
    return boto3.client('cognito-idp')


def send_cognito_command(command, arguments):
    try:
        if arguments is None:
            arguments = {}

        logger.debug("Sending Cognito command '%s'" % command,
                     extra={'arguments': arguments})

        client = open_cognito_connection()
        response = getattr(client, command)(
            **arguments
        )
    except ClientError as e:
        if not e.response['Error']['Code'] == 'UsernameExistsException':
            logger.error("Error sending command to Cognito: %s" % str(e))
            logger.exception(e)

        raise e

    return response


def create_user(username, password):
    args = {
        'ClientId': get_setting('COGNITO_USER_POOL_CLIENT_USERS_ID'),
        'Username': username,
        'Password': password
    }

    return send_cognito_command(SIGN_UP, arguments=args)
