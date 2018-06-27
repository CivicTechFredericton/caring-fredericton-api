#!/usr/bin/env python
# pylint: disable=invalid-name
from __future__ import print_function
import argparse
import os
import sys
import boto3

# Read input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--environment', required=True, help="Environment identifier, such as 'eric', "
                                                               "'dev', 'stage', etc.")
parser.add_argument('-p', '--profile', required=False)
parser.add_argument('-r', '--region', required=False)
parser.add_argument('-u', '--update', action='store_true')

args = vars(parser.parse_args())
environment = args['environment']
profile = args.get('profile')
region = args.get('region')
update = args.get('update')

prefix = 'caring-fred'
stack_name = '{}-{}-dynamo-tables'.format(prefix, environment)

template = '{}/{}/{}'.format(os.path.dirname(os.path.realpath(__file__)),
                              environment,
                              'dynamo_tables.yaml')
parameters = {}
tags = {"CLIENT": "Civic Tech", "PROJECT": "Caring Calendar"}

if not profile and not region:
    print('Missing input: Must specify either --profile or --region', file=sys.stderr)
    parser.print_usage()
    sys.exit(1)

cfn_client = boto3.Session(profile_name=profile, region_name=region).client('cloudformation')

# Create stack
with open(template) as template_body:
    arguments = {
        'Capabilities': ['CAPABILITY_NAMED_IAM'],
        'StackName': stack_name,
        'TemplateBody': template_body.read(),
        'Parameters': [{'ParameterKey': k, 'ParameterValue': v} for k, v in parameters.items()],
        'Tags': [{'Key': k, 'Value': v} for k, v in tags.items()]
    }

if update:
    cfn_client.update_stack(**arguments)
else:
    cfn_client.create_stack(**arguments)
