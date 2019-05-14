#!/usr/bin/env python
import argparse
import boto3
import os

PREFIX = 'punch-it-api'

# =======================================================================
# Read input parameters
# =======================================================================
os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', required=True,
                    help='AWS CLI region to use')
parser.add_argument('-s', '--stage',
                    help='Stage name or environment such as dev, stage, uat, etc.', required=True)
args = parser.parse_args()

# =======================================================================
# Initialize boto3
# =======================================================================
session = boto3.Session(region_name=args.region)

# Find the details of the user pool
stage = args.stage
user_pool_name = '{}-{}-users'.format(PREFIX, stage)


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

# Get the list of users
response = cognito_idp_client.list_users(
    UserPoolId=user_pool_id
)

for cognito_user in response['Users']:
    username = cognito_user['Username']
    attributes = cognito_user['Attributes']
    for curr_attribute in attributes:
        if curr_attribute['Name'] == 'email':
            print(f"Removing user {curr_attribute['Value']}")
    cognito_idp_client.admin_delete_user(
        UserPoolId=user_pool_id,
        Username=username
    )


