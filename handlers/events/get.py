import json

from pynamodb.exceptions import DoesNotExist

from core.db.events import EventModel
from handlers.api_utils import set_dynamo_table_name
from services.events import get_event_occurrence
from services.events.resource import event_occurrence_details_schema


def handler(event, context):
    set_dynamo_table_name(EventModel)

    owner = event['path']['org_id']
    event_id = event['path']['event_id']
    occurrence = int(event['path']['occurrence'])

    try:
        found_event = EventModel.get(hash_key=event_id, range_key=owner)
        occurrence = get_event_occurrence(found_event, occurrence)

        return event_occurrence_details_schema.dump(occurrence).data

        # return {
        #     'statusCode': 200,
        #     'headers': {
        #         'Access-Control-Allow-Origin': '*',
        #         'Access-Control-Allow-Credentials': True,
        #     },
        #     'body': event_occurrence_details_schema.dump(occurrence).data
        # }
    except DoesNotExist:
        message = 'Event {} for owner {} does not exist'.format(event_id, owner)
        return {
            'statusCode': 404,
            'body': json.dumps({'error_message': message})
        }
