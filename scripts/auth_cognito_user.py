#!/usr/bin/env python
import argparse
import os
import boto3

os.chdir(os.path.dirname(os.path.realpath(__file__)))

PREFIX = 'caring-fred'

# =======================================================================
# Read input parameters
# =======================================================================
parser = argparse.ArgumentParser()
parser.add_argument('login', type=str, help='User login')
parser.add_argument('password', type=str, help='User password')
parser.add_argument('-p', '--profile', required=True,
                    help='AWS CLI profile to use')
parser.add_argument('-s', '--stage',
                    help='Stage name or environment such as dev, stage, uat, etc.', required=True)
args = parser.parse_args()

# =======================================================================
# Initialize boto3
# =======================================================================
session = boto3.Session(profile_name=args.profile)
cognito_idp_client = session.client('cognito-idp')

# =======================================================================
# Set variables
# =======================================================================
username = args.login
password = args.password

# Find the details of the user pool
stage = args.stage
user_pool_name = '{}-{}-users'.format(PREFIX, stage)
app_client_name = 'users'

response = cognito_idp_client.list_user_pools(
    MaxResults=60
)

for user_pool in response['UserPools']:
    if user_pool['Name'] == user_pool_name:
        user_pool_id = user_pool['Id']
        break


if user_pool_id:
    # Find the associated client id
    response = cognito_idp_client.list_user_pool_clients(
        UserPoolId=user_pool_id,
        MaxResults=60
    )

    for user_pool_client in response['UserPoolClients']:
        if user_pool_client['ClientName'] == app_client_name:
            client_id = user_pool_client['ClientId']
            break

    if client_id:
        response = cognito_idp_client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
        )

        if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
            response = cognito_idp_client.admin_respond_to_auth_challenge(
                UserPoolId=user_pool_id,
                ClientId= client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'NEW_PASSWORD': password,
                },
                Session=response['Session'],
            )

        # Print the retrieved token
        print(response.get('AuthenticationResult', {}).get('IdToken'))
    else:
        print('No matching app client defined for user pool id {}'.format(user_pool_id))
else:
    print('No user pool exists with name {}'.format(user_pool_name))
