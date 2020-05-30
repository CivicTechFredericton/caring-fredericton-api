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
stage = args.stage

user_pool_name = '{}-{}-users'.format(PREFIX, stage)

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

response = cognito_idp_client.describe_user_pool(
    UserPoolId=user_pool_id
)

app_client_name = 'users'
client_id = None
response = cognito_idp_client.list_user_pool_clients(
    UserPoolId=user_pool_id,
    MaxResults=60
)

for user_pool_client in response['UserPoolClients']:
    if user_pool_client['ClientName'] == app_client_name:
        client_id = user_pool_client['ClientId']
        break

response = cognito_idp_client.describe_user_pool_client(
    UserPoolId=user_pool_id,
    ClientId=client_id
)

account_id = session.client('sts').get_caller_identity().get('Account')
print('Pool ARN: arn:aws:cognito-idp:{}:{}:userpool/{}'.format(args.region, account_id, user_pool_id))
print('Pool ID: {}'.format(user_pool_id))
print('Client ID: {}'.format(client_id))
