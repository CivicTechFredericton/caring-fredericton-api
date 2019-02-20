from dateutil.relativedelta import relativedelta

from core import errors
from core.db import save_with_unique_id
from core.db.events.model import EventModel


# -------------------------
# Event creation
# -------------------------
from services.events import constants


def create_event(**event_args):
    # Set the number of occurrences
    set_occurrences(event_args)

    # Save the object
    event = EventModel(**event_args)
    save_with_unique_id(event)

    return event


# -------------------------
# Set occurrences on save
# -------------------------
def set_occurrences(event_args):
    # Check to see if the recurrence details is set
    if event_args['is_recurring']:
        recurrence_details = event_args.get('recurrence_details')
        if recurrence_details is None:
            message = 'Missing data for required field when is_recurring is true'
            raise errors.ResourceValidationError(messages={'recurrence_details': [message]})
    else:
        event_args['recurrence_details'] = None
        recurrence_details = set_default_recurrence_details()

    # Populate the occurrences list and last end date
    last_end_date, occurrences = populate_occurrences(event_args['start_date'],
                                                      event_args['end_date'],
                                                      recurrence_details)

    event_args['end_date'] = last_end_date
    event_args['occurrences'] = occurrences


def set_default_recurrence_details():
    return {
        'recurrence': constants.RecurrenceType.DAILY.value,
        'num_recurrences': constants.MIN_RECURRENCE
    }


def populate_occurrences(start_date, end_date, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    occurrences = []

    for i in range(recurrence_details['num_recurrences']):
        curr_start_date, curr_end_date = set_occurrence_date(start_date,
                                                             end_date,
                                                             i * day_separation,
                                                             i * week_separation,
                                                             i * month_separation)

        occurrences.append(get_occurrence_entry(i + 1, curr_start_date, curr_end_date))

    return curr_end_date, occurrences


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
