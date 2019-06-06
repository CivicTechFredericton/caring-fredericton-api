#!/usr/bin/env python
import argparse
import boto3
import os

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, JSONAttribute, UTCDateTimeAttribute
from pynamodb.indexes import KeysOnlyProjection, GlobalSecondaryIndex
from pynamodb.models import Model


class SearchNameIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'search_name-index'
        projection = KeysOnlyProjection()
        read_capacity_units = 0
        write_capacity_units = 0

    search_name = UnicodeAttribute(hash_key=True)


class OrganizationModel(Model):
    class Meta:
        region = 'ca-central-1'
        simple_name = 'organization'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    search_name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone = UnicodeAttribute()
    administrator_id = UnicodeAttribute()
    address = JSONAttribute(null=True)
    is_verified = BooleanAttribute(default=False)
    search_name_index = SearchNameIndex()
    created_at = UTCDateTimeAttribute()
    created_by = UnicodeAttribute()
    updated_at = UTCDateTimeAttribute()
    updated_by = UnicodeAttribute()


# =======================================================================
# Read input parameters
# =======================================================================
os.chdir(os.path.dirname(os.path.realpath(__file__)))

PREFIX = 'caring-fred'

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

stage = args.stage
organization_table_name = '{}-{}-organization'.format(PREFIX, stage)

# Set the model names
OrganizationModel.Meta.table_name = organization_table_name

# Update each record to set the display name
organization_list = OrganizationModel.scan()
for organization in organization_list:
    if not organization.search_name:
        organization_name = organization.name
        print(f"Setting search name for organization {organization_name}")
        actions = [OrganizationModel.search_name.set(organization_name.lower())]
        organization.update(actions=actions)

print('Organization records updated')
