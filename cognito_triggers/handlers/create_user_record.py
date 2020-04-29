from datetime import timezone

import boto3
import datetime
import os


def handler(event, context):
    """
    Function to be invoked by a Cognito Post Confirmation trigger to populate the
    user's extended information in DynamoDB
    :param event:
    :param context:
    :return:
    """
    user_attributes = event['request']['userAttributes']
    user_sub = user_attributes['sub']

    # Create a new DynamoDB record for the current user
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['USER_TABLE'])
    record = table.get_item(
        Key={'id': user_sub}
    )

    if 'Item' not in record:
        # Set the current date and time for the record
        dt = datetime.datetime.now()
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.isoformat()

        # Set the create and update user for the record
        create_user = context.aws_request_id

        table.put_item(
            Item={
                'id': user_sub,
                'email': user_attributes['email'],
                'first_name': user_attributes['given_name'],
                'last_name': user_attributes['family_name'],
                'active': True,
                'created_at': utc_timestamp,
                'created_by': create_user,
                'updated_at': utc_timestamp,
                'updated_by': create_user
            }
        )

        # Remove the temporary attributes
        cognito_idp = boto3.client('cognito-idp')
        cognito_idp.admin_delete_user_attributes(
            UserPoolId=os.environ['COGNITO_USER_POOL_USERS_ID'],
            Username=user_sub,
            UserAttributeNames=[
                'family_name', 'given_name'
            ]
        )

    # Return flow back to Amazon Cognito
    return event
