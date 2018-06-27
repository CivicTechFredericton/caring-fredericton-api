#!/usr/bin/env python
import argparse
import os

import boto3

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# =======================================================================
# Read input parameters
# =======================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--profile',
                    help='AWS CLI profile to use', required=True)
parser.add_argument(
    '-s', '--stage', help='Stage name or environment such as dev, stage, uat, etc.', required=True)

args = vars(parser.parse_args())

# =======================================================================
# Initialize boto3
# =======================================================================
session = boto3.Session(profile_name=args['profile'])
cognito_idp_client = session.client('cognito-idp')
account_id = session.client('sts').get_caller_identity().get('Account')
region = session.region_name

# =======================================================================
# Set variables
# =======================================================================
stage = args['stage']
prefix = 'caring-fred'
user_pool_name = '{}-{}'.format(prefix, stage)

# -----------------------------------------------------------------------
# Construct email verification message
# -----------------------------------------------------------------------
email_verification_message = "Your verification code is {####}.\n\n"

# -----------------------------------------------------------------------
# Construct invite email message
# -----------------------------------------------------------------------
invite_email_message = "Your username is {username} and temporary password is {####}.\n\n"

# =======================================================================
# Create the resources
# =======================================================================
user_pool_id = ''
client_id = ''

response = cognito_idp_client.list_user_pools(MaxResults=60)
for user_pool in response['UserPools']:
    if user_pool['Name'] == user_pool_name:
        user_pool_id = user_pool['Id']
        break

if not user_pool_id:
    response = cognito_idp_client.create_user_pool(
        PoolName=user_pool_name,
        Policies={
            'PasswordPolicy': {
                'MinimumLength': 8,
                'RequireUppercase': False,
                'RequireLowercase': True,
                'RequireNumbers': True,
                'RequireSymbols': False
            }
        },
        AutoVerifiedAttributes=[
            'email'
        ],
        UsernameAttributes=[
            'email'
        ],
        EmailVerificationMessage=email_verification_message,
        EmailVerificationSubject='Your verification code',
        UserPoolTags={
            'CLIENT': 'Civic Tech',
            'PROJECT': 'Caring Calendar'
        },
        AdminCreateUserConfig={
            'AllowAdminCreateUserOnly': True,
            'InviteMessageTemplate': {
                'EmailMessage': invite_email_message,
                'EmailSubject': 'Your temporary password'
            }
        }
    )

    user_pool_id = response['UserPool']['Id']

response = cognito_idp_client.list_user_pool_clients(
    UserPoolId=user_pool_id,
    MaxResults=60
)
for user_pool_client in response['UserPoolClients']:
    if user_pool_client['ClientName'] == user_pool_name:
        client_id = user_pool_client['ClientId']
        break

if not client_id:
    response = cognito_idp_client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=user_pool_name,
        RefreshTokenValidity=30,
        ExplicitAuthFlows=[
            'ADMIN_NO_SRP_AUTH'
        ]
    )

    client_id = response['UserPoolClient']['ClientId']

print('Pool ARN: arn:aws:cognito-idp:{}:{}:userpool/{}'.format(region, account_id, user_pool_id))
print('Pool ID: {}'.format(user_pool_id))
print('Client ID: {}'.format(client_id))
