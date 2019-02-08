import json

from dateutil import parser
from core.db.events import EventModel
from handlers.api_utils import set_dynamo_table_name
from services.events import set_category_filter, set_dates_filter, get_recurring_events_list
from services.events.resource import event_list_schema


def handler(event, context):
    """
    List the events in the system agnostic to any owner
    :return: The list of events in the system
    """
    set_dynamo_table_name(EventModel)

    query_params = event.get('queryStringParameters', {})
    # query_params = event.get('queryString', {})

    events_list = EventModel.scan()
    return get_events_response(events_list, query_params)


def get_events_response(events_list, query_params):
    # Set the filters
    filter_start_date, filter_end_date = set_dates_filter(get_date_query_string_param(query_params.get('start_date')),
                                                          get_date_query_string_param(query_params.get('end_date')))
    filter_categories = set_category_filter(query_params.get('categories'))

    response_list = []
    for event in events_list:
        occurrences = get_recurring_events_list(event, filter_start_date, filter_end_date, filter_categories)
        for occurrence in occurrences:
            response_list.append(event_list_schema.dump(occurrence).data)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps({'items': response_list})
    }


def get_date_query_string_param(param):
    if not param:
        return None

    return parser.parse(param)
