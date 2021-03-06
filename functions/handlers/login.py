import json
import os

import boto3


def handler(event, context):
    """
    This function authenticates user information against a user pool
    :param event: The object containing the request details (query strings, body, etc.)
    :param context: The object containing runtime information (request ID, CloudWatch log group, etc.)
    :return: The authentication token of the user if verified
    """
    data = json.loads(event['body'])

    if 'username' not in data:
        return {'statusCode': 422,
                'body': json.dumps({
                    'error_message': 'Missing username value'
                })
                }

    if 'password' not in data:
        return {'statusCode': 422,
                'body': json.dumps({
                    'error_message': 'Missing password value'
                })
                }

    cognito = boto3.client('cognito-idp')
    try:
        # Authenticate the user
        user_pool_id = os.environ['COGNITO_USER_POOL_USERS_ID']
        client_id = os.environ['COGNITO_USER_POOL_CLIENT_USERS_ID']
        username = data['username']
        password = data['password']

        response = cognito.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
        )

        if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
            return get_error_response()

        token_details = {
            'authToken': response.get('AuthenticationResult').get('IdToken')
        }

        return {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            "body": json.dumps(token_details)
        }
    except (cognito.exceptions.UserNotFoundException, cognito.exceptions.NotAuthorizedException,
            cognito.exceptions.InvalidParameterException):
        return get_error_response()


def get_error_response():
    return {
        'statusCode': 401,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'error_message': 'Invalid username or password'
            })
    }
