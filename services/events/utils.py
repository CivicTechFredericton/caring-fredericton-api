import pendulum

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

        start_date = pendulum.parse(event_args['start_date'].strftime(constants.EVENT_DATE_FORMAT), strict=False)
        num_recurrences = recurrence_details['num_recurrences']

        occurrences = []
        recurrence = recurrence_details['recurrence']
        if recurrence == constants.RecurrenceType.DAILY.value:
            occurrences = [add_day_to_date(start_date, i) for i in range(num_recurrences)]
        if recurrence == constants.RecurrenceType.WEEKLY.value:
            occurrences = [add_week_to_date(start_date, i) for i in range(num_recurrences)]
        if recurrence == constants.RecurrenceType.BI_WEEKLY.value:
            occurrences = [add_week_to_date(start_date, i*2) for i in range(num_recurrences)]
        if recurrence == constants.RecurrenceType.MONTHLY.value:
            occurrences = [add_month_to_date(start_date, i) for i in range(num_recurrences)]

        # TODO: Consider adding the occurrences in a separate table
        event_args['occurrences'] = occurrences


def add_day_to_date(date, num_days):
    date = date.add(days=num_days)
    return date.strftime(constants.EVENT_DATE_FORMAT)


def add_week_to_date(date, num_weeks):
    date = date.add(weeks=num_weeks)
    return date.strftime(constants.EVENT_DATE_FORMAT)


def add_month_to_date(date, num_months):
    date = date.add(months=num_months)
    return date.strftime(constants.EVENT_DATE_FORMAT)
