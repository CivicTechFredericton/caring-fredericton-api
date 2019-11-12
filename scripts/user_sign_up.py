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
parser.add_argument('first_name', type=str, help='User first name')
parser.add_argument('last_name', type=str, help='User last name')
parser.add_argument('-r', '--region', required=False,
                    default='ca-central-1', help='AWS CLI region to use')
parser.add_argument('-s', '--stage',
                    help='Stage name or environment such as dev, stage, uat, etc.', required=True)
args = parser.parse_args()

# =======================================================================
# Initialize boto3
# =======================================================================
session = boto3.Session(region_name=args.region)

# =======================================================================
# Set variables
# =======================================================================
username = args.login
password = args.password
first_name = args.first_name
last_name = args.last_name
stage = args.stage

user_pool_name = '{}-{}-users'.format(PREFIX, stage)
user_table_name = '{}-{}-user'.format(PREFIX, stage)
app_client_name = 'users'

# Find the details of the user pool
cognito_idp_client = session.client('cognito-idp')
response = cognito_idp_client.list_user_pools(
    MaxResults=60
)

user_pool_id = None
for user_pool in response['UserPools']:
    if user_pool['Name'] == user_pool_name:
        user_pool_id = user_pool['Id']
        break

if not user_pool_id:
    print('No user pool exists with name {}'.format(user_pool_name))
    exit()

# Create the user
arguments = {
    'Username': username,
    'TemporaryPassword': password,
    'UserAttributes': [
        {
            'Name': 'email',
            'Value': username
        },
        {
            'Name': 'email_verified',
            'Value': 'true'
        }
    ],
    'MessageAction': 'SUPPRESS'
}

try:
    response = cognito_idp_client.admin_create_user(
        UserPoolId=user_pool_id,
        **arguments
    )
except Exception as e:
    if e.response['Error']['Code'] == 'UsernameExistsException':
        print(f"User with name '{username}' already in use; please enter a different value")
        exit()

# Retrieve the stored username
username_sub = response['User']['Username']

# Authenticate the user
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
            ClientId=client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={
                'USERNAME': username,
                'PASSWORD': password,
                'NEW_PASSWORD': password,
            },
            Session=response['Session'],
        )
else:
    print('No matching app client defined for user pool id {}'.format(user_pool_id))
    exit()

# Create the DynamoDB user record
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(user_table_name)
table.put_item(
    Item={
        'id': username_sub,
        'email': username,
        'first_name': first_name,
        'last_name': last_name
    }
)

print('User Created')
