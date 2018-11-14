import pendulum

from core import errors
from services.events import constants
from webargs import missing


# -------------------------
# Set occurrences on save
# -------------------------
def set_occurrences(event_args):
    if event_args['is_recurring']:
        # Look for the recurrence details
        recurrence_details = event_args['recurrence_details']
        if recurrence_details is missing:
            message = 'Missing data for required field'
            raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

        start_date = pendulum.instance(event_args['start_date'])
        occurrences, new_end_date = populate_occurrences(start_date, recurrence_details)

        # Update the occurrences and end date to reflect the last occurrence
        event_args['occurrences'] = occurrences
        event_args['end_date'] = new_end_date


def populate_occurrences(start_date, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    last_occurrence_date = start_date
    occurrences = []
    for i in range(recurrence_details['num_recurrences']):
        last_occurrence_date = start_date.add(days=i*day_separation,
                                              weeks=i*week_separation,
                                              months=i*month_separation)
        occurrences.append(last_occurrence_date.strftime(constants.EVENT_DATE_FORMAT))

    return occurrences, last_occurrence_date


def base_daily_interval():
    return 1, 0, 0


def base_weekly_interval():
    return 0, 1, 0


def base_bi_weekly_interval():
    return 0, 2, 0


def base_monthly_interval():
    return 0, 0, 1


def define_interval_increments(recurrence):
    switcher = {
        constants.RecurrenceType.DAILY.value: base_daily_interval(),
        constants.RecurrenceType.WEEKLY.value: base_weekly_interval(),
        constants.RecurrenceType.BI_WEEKLY: base_bi_weekly_interval(),
        constants.RecurrenceType.MONTHLY.value: base_monthly_interval()
    }

    # Get the function from switcher dictionary
    return switcher.get(recurrence, lambda: "Invalid Interval Value")


# -------------------------
# List occurrences on read
# -------------------------
def get_recurring_events_list(event):
    occurrences = event.occurrences
    if occurrences is not None:
        return [get_recurring_event(event, occurrence) for occurrence in occurrences]
    else:
        return [event]


def get_recurring_event(event, occurrence):
    date = pendulum.parse(occurrence, strict=False)
    event.start_date = date
    event.end_date = date

    return event

