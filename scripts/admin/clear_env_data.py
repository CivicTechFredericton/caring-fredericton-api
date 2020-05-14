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
dynamodb = boto3.resource('dynamodb')
cognito_idp_client = session.client('cognito-idp')

# =======================================================================
# Set variables
# =======================================================================
stage = args.stage


# Remove the data from the tables
def delete_table_data(table_name):
    db_table = dynamodb.Table(table_name)
    scan = None

    with db_table.batch_writer() as batch:
        count = 0
        while scan is None or 'LastEvaluatedKey' in scan:
            if scan is not None and 'LastEvaluatedKey' in scan:
                scan = db_table.scan(
                    ProjectionExpression='id',
                    ExclusiveStartKey=scan['LastEvaluatedKey'],
                )
            else:
                scan = db_table.scan(ProjectionExpression='id')

            for item in scan['Items']:
                if count % 5000 == 0:
                    print(count)
                batch.delete_item(Key={'id': item['id']})
                count = count + 1


# Return the entire list of items from Cognito
def boto3_paginate(method_to_paginate, **params_to_pass):
    boto_response = method_to_paginate(**params_to_pass)
    yield boto_response
    while boto_response.get('PaginationToken', None):
        boto_response = method_to_paginate(PaginationToken=boto_response['PaginationToken'], **params_to_pass)
        yield boto_response


delete_table_data('{}-{}-user'.format(PREFIX, stage))
delete_table_data('{}-{}-organization'.format(PREFIX, stage))
delete_table_data('{}-{}-event'.format(PREFIX, stage))

# Remove the data from the Cognito user pool
user_pool_name = '{}-{}-users'.format(PREFIX, stage)

response = cognito_idp_client.list_user_pools(
    MaxResults=60
)

user_pool_id = None
for user_pool in response['UserPools']:
    if user_pool['Name'] == user_pool_name:
        user_pool_id = user_pool['Id']
        break

# response = cognito_idp_client.list_users(
#     UserPoolId=user_pool_id,
# )

users = []

# if `Limit` is not provided - the api will return 60 items, which is maximum
for page in boto3_paginate(cognito_idp_client.list_users, UserPoolId=user_pool_id):
    users += page['Users']

for user in users:
    # print(user['Username'])
    cognito_idp_client.admin_delete_user(
        UserPoolId=user_pool_id,
        Username=user['Username']
    )

