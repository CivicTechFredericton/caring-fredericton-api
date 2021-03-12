#!/usr/bin/env python
import argparse
import boto3
import csv
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

PREFIX = 'caring-fred'
REQUIRED_ATTRIBUTES = ['Username', 'email', 'email_verified', 'given_name', 'family_name']
CSV_FILE_NAME = 'cognito_users.csv'

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
dynamodb = boto3.resource('dynamodb')
cognito_idp_client = session.client('cognito-idp')

# =======================================================================
# Set variables
# =======================================================================
stage = args.stage

# Find the details of the user pool
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

# Set the DynamoDB table details
user_table_name = '{}-{}-user'.format(PREFIX, stage)
user_table = dynamodb.Table(user_table_name)

# Read the lines in the CSV file
with open(CSV_FILE_NAME, 'r') as csv_file:
    # Read in the contents of the file
    csv_dict_reader = csv.DictReader(csv_file,
                                     fieldnames=REQUIRED_ATTRIBUTES)

    # Skip the headers
    next(csv_dict_reader, None)

    for row in csv_dict_reader:
        original_user_sub = row['Username']
        username = row['email']

        # Create a new Cognito user record
        arguments = {
            'Username': username,
            'UserAttributes': [
                {
                    'Name': 'email',
                    'Value': username
                },
                {
                    'Name': 'email_verified',
                    'Value': row['email_verified']
                }
            ]
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

        # Get the original user record
        old_record = user_table.get_item(
            Key={'id': original_user_sub}
        )

        if 'Item' in old_record:
            user_details = old_record['Item']

            user_item = {
                'id': username_sub,
                'email': user_details['email'],
                'first_name': user_details['first_name'],
                'last_name': user_details['last_name'],
                'active': user_details['active'],
                'created_at': user_details['created_at'],
                'created_by': user_details['created_by'],
                'updated_at': user_details['updated_at'],
                'updated_by': user_details['updated_by']
            }

            # Update the organization details
            if 'organization_id' in user_details:
                user_item['organization_id'] = user_details['organization_id']

            if 'organization_name' in user_details:
                user_item['organization_name'] = user_details['organization_name']

            # Create a new record
            user_table.put_item(
                Item=user_item
            )

            # Remove the original user record
            user_table.delete_item(
                Key={'id': original_user_sub}
            )

    csv_file.close()
