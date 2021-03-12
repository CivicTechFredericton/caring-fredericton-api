#!/usr/bin/env python
import argparse
import boto3
import csv
# import datetime
# import json
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


# Return the entire list of items from Cognito
def boto3_paginate(method_to_paginate, **params_to_pass):
    boto_response = method_to_paginate(**params_to_pass)
    yield boto_response
    while boto_response.get('PaginationToken', None):
        boto_response = method_to_paginate(PaginationToken=boto_response['PaginationToken'], **params_to_pass)
        yield boto_response


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

if not user_pool_id:
    print('No user pool exists with name {}'.format(user_pool_name))
    exit()

users = []

# if `Limit` is not provided - the api will return 60 items, which is maximum
for page in boto3_paginate(cognito_idp_client.list_users, UserPoolId=user_pool_id):
    users += page['Users']


# def datetimeconverter(o):
#     if isinstance(o, datetime.datetime):
#         return str(o)
#
#
# json_formatted_str = json.dumps(users, indent=4, default=datetimeconverter)
# print(json_formatted_str)


csv_new_line = {REQUIRED_ATTRIBUTES[i]: '' for i in range(len(REQUIRED_ATTRIBUTES))}
# TODO: Add error handling
with open(CSV_FILE_NAME, 'w') as csv_file:
    # csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # for user in users:
    #     """ Fetch Required Attributes Provided """
    #     csv_line = csv_new_line.copy()
    #     for required_attr in REQUIRED_ATTRIBUTES:
    #         csv_line[required_attr] = ''
    #         if required_attr in user.keys():
    #             csv_line[required_attr] = str(user[required_attr])
    #             continue
    #         for usr_attr in user['Attributes']:
    #             if usr_attr['Name'] == required_attr:
    #                 csv_line[required_attr] = str(usr_attr['Value'])
    #
    #     csv_writer.writerow(",".join(csv_line.values()))
    # employee_writer.writerow(['Erica Meyers', 'IT', 'March'])

    csv_file.write(",".join(csv_new_line.keys()) + '\n')
    csv_lines = []
    for user in users:
        """ Fetch Required Attributes Provided """
        csv_line = csv_new_line.copy()
        for required_attr in REQUIRED_ATTRIBUTES:
            csv_line[required_attr] = ''
            if required_attr in user.keys():
                csv_line[required_attr] = str(user[required_attr])
                continue
            for usr_attr in user['Attributes']:
                if usr_attr['Name'] == required_attr:
                    csv_line[required_attr] = str(usr_attr['Value'])

        csv_lines.append(",".join(csv_line.values()) + '\n')

    csv_file.writelines(csv_lines)
    csv_file.close()

# print()
# print("Listing Cognito users")
# print()
# for user in users:
#     username = user['Username']
#     # print(f'Username: {username}')
#     print(user)
#
