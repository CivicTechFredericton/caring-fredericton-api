import copy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from webargs import missing

from core import errors
from services.events import constants


# -------------------------
# Handle filter conditions
# -------------------------
def set_filter_dates(start_date, end_date):
    if not start_date and not end_date:
        today = datetime.today()
        filter_date = datetime(today.year, today.month, today.day)
        return filter_date, filter_date + relativedelta(days=+7)
    if start_date and not end_date:
        return start_date, start_date + relativedelta(days=+7)
    if not start_date and end_date:
        return end_date + relativedelta(days=-7), end_date

    return start_date, end_date


# -------------------------
# Set occurrences on save
# -------------------------
def set_occurrences(event_args):
    if event_args['is_recurring']:
        event_args['occurrences'] = populate_occurrences(event_args)
    else:
        # Populate a single occurrence
        event_args['recurrence_details'] = None
        event_args['occurrences'] = [get_occurrence_entry(1, event_args['start_date'], event_args['end_date'])]


def populate_occurrences(event_args):
    # Look for the recurrence details
    recurrence_details = event_args['recurrence_details']
    if recurrence_details is missing:
        message = 'Missing data for required field'
        raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])
    start_date = event_args['start_date']
    end_date = event_args['end_date']

    occurrences = []

    for i in range(recurrence_details['num_recurrences']):
        curr_start_date, curr_end_date = set_occurrence_date(start_date,
                                                             end_date,
                                                             i * day_separation,
                                                             i * week_separation,
                                                             i * month_separation)

        occurrences.append(get_occurrence_entry(i + 1, curr_start_date, curr_end_date))

    event_args['end_date'] = curr_end_date

    return occurrences


def get_occurrence_entry(occurrence_num, start_date, end_date):
    return {
        'occurrence_num': occurrence_num,
        'start_date': start_date,
        'end_date': end_date
    }


def set_occurrence_date(start_date, end_date, day_separation, week_separation, month_separation):
    new_start_date = start_date + relativedelta(day=+day_separation,
                                                weeks=+week_separation,
                                                months=+month_separation)

    new_end_date = end_date + relativedelta(day=+day_separation,
                                            weeks=+week_separation,
                                            months=+month_separation)

    return new_start_date, new_end_date


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
        constants.RecurrenceType.BI_WEEKLY.value: base_bi_weekly_interval(),
        constants.RecurrenceType.MONTHLY.value: base_monthly_interval()
    }

    # Get the function from switcher dictionary
    return switcher.get(recurrence, lambda: "Invalid Interval Value")


# -------------------------
# List occurrences on read
# -------------------------
def get_recurring_events_list(event, start_date, end_date):
    return [get_recurring_event(event, occurrence) for occurrence in event.occurrences
            if within_date_range(occurrence, start_date, end_date)]


def within_date_range(occurrence, start_date, end_date):
    return start_date <= occurrence.start_date <= end_date or \
           start_date <= occurrence.end_date <= end_date


def get_recurring_event(event, occurrence):
    # Perform a deep copy of the event object so that unique objects are inserted in the list
    new_event = copy.deepcopy(event)
    new_event.start_date = occurrence.start_date
    new_event.end_date = occurrence.end_date

    return new_event

