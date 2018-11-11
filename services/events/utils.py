import datetime

from core import errors
from services.events import constants
from webargs import missing


def set_occurrences(event_args):
    if event_args['is_recurring']:
        # Loom for the recurrence details
        recurrence_details = event_args['recurrence_details']
        if recurrence_details is missing:
            message = 'Missing data for required field'
            raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

        start_date = event_args['start_date']
        # print(start_date.weekday())
        num_recurrences = recurrence_details['num_recurrences']

        occurrences = []
        recurrence = recurrence_details['recurrence']
        if recurrence == constants.RecurrenceType.DAILY.value:
            occurrences = [add_day_to_date(start_date, i) for i in range(num_recurrences)]

        event_args['occurrences'] = occurrences


def add_day_to_date(start_date, num_days):
    t = start_date + datetime.timedelta(days=num_days)
    return t.strftime(constants.EVENT_DATE_FORMAT)

