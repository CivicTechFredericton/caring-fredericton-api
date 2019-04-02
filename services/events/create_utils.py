from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

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
        'occurrence_type': constants.OccurrenceType.AFTER.value,
        'num_recurrences': constants.MIN_RECURRENCE
    }


def populate_occurrences(start_date, end_date, recurrence_details):
    occurrence_type = recurrence_details['occurrence_type']

    if occurrence_type == constants.OccurrenceType.NEVER.value:
        last_end_date, occurrences = generate_occurrence_type_never_events(start_date, end_date, recurrence_details)

    elif occurrence_type == constants.OccurrenceType.AFTER.value:
        last_end_date, occurrences = generate_occurrence_type_after_events(start_date, end_date, recurrence_details)

    elif occurrence_type == constants.OccurrenceType.ON.value:
        last_end_date, occurrences = generate_occurrence_type_on_events(start_date, end_date, recurrence_details)

    else:
        message = 'Invalid value, must be one of {}'.format(constants.OccurrenceType.values())
        raise errors.ResourceValidationError(messages={'occurrence_type': [message]})

    return last_end_date, occurrences


def generate_occurrence_type_never_events(start_date, end_date, recurrence_details):
    # TODO: Remove limitation when data model allows for occurrences to never end
    recurrence_details['num_recurrences'] = constants.MAX_RECURRENCE

    return generate_occurrence_type_after_events(start_date, end_date, recurrence_details)


def generate_occurrence_type_after_events(start_date, end_date, recurrence_details):
    occurrences = []

    day_of_week, week_of_month, separation_count = get_relative_interval_details(recurrence_details)

    if day_of_week and week_of_month:
        for occurrence_num in range(recurrence_details['num_recurrences']):
            curr_start_date, curr_end_date = set_relative_occurrence_date(start_date,
                                                                          end_date,
                                                                          day_of_week,
                                                                          week_of_month,
                                                                          occurrence_num * separation_count)

            occurrences.append(get_occurrence_entry(occurrence_num + 1, curr_start_date, curr_end_date))

    else:
        # Check to see if the event begins on the 28th of February
        # is_start_end_february = is_event_start_end_february(start_date)

        day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])
        for occurrence_num in range(recurrence_details['num_recurrences']):
            curr_start_date, curr_end_date = set_absolute_occurrence_date(start_date,
                                                                          end_date,
                                                                          occurrence_num * day_separation,
                                                                          occurrence_num * week_separation,
                                                                          occurrence_num * month_separation)

            occurrences.append(get_occurrence_entry(occurrence_num + 1, curr_start_date, curr_end_date))

    return curr_end_date, occurrences


def generate_occurrence_type_on_events(start_date, end_date, recurrence_details):
    # TODO: Determine the number of occurrences between the start_date and the specified occurrence end date?
    occurrences = []

    on_end_date = recurrence_details.get('on_end_date')
    day_of_week, week_of_month, separation_count = get_relative_interval_details(recurrence_details)

    occurrence_num = 0

    if day_of_week and week_of_month:
        while curr_start_date < on_end_date:
            curr_start_date, curr_end_date = set_relative_occurrence_date(start_date,
                                                                          end_date,
                                                                          day_of_week,
                                                                          week_of_month,
                                                                          occurrence_num * separation_count)

            occurrences.append(get_occurrence_entry(occurrence_num + 1, curr_start_date, curr_end_date))

    else:
        # Check to see if the event begins on the 28th of February
        # is_start_end_february = is_event_start_end_february(start_date)

        day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

        while curr_start_date < on_end_date:
            curr_start_date, curr_end_date = set_absolute_occurrence_date(start_date,
                                                                          end_date,
                                                                          occurrence_num * day_separation,
                                                                          occurrence_num * week_separation,
                                                                          occurrence_num * month_separation)

            occurrences.append(get_occurrence_entry(occurrence_num + 1, curr_start_date, curr_end_date))

    return curr_end_date, occurrences


# def is_event_start_end_february(start_date):
#     return start_date.month == 2 and start_date.day == 28


def get_occurrence_entry(occurrence_num, start_date, end_date):
    return {
        'occurrence_num': occurrence_num,
        'start_date': start_date,
        'end_date': end_date
    }


# ------------------------------------
# Absolute Event Interval Functions
# ------------------------------------
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


# ------------------------------------
# Relative Event Interval Functions
# ------------------------------------
def get_relative_interval_details(recurrence_details):
    return recurrence_details.get('day_of_week'), \
           recurrence_details.get('week_of_month'), \
           recurrence_details.get('separation_count')


def set_absolute_occurrence_date(start_date, end_date, day_separation, week_separation, month_separation):
    """
    Sets the absolute date intervals for DAILY, WEEKLY, BI_WEEKLY, and MONTHLY frequency
    For example: Every 3rd of the month
    :param start_date: The current start date
    :param end_date: The current end date
    :param day_separation: The number of days between events
    :param week_separation: The number of weeks between events
    :param month_separation:  The number of months between events
    :return:
    """
    new_start_date = start_date + relativedelta(day=+day_separation,
                                                weeks=+week_separation,
                                                months=+month_separation)

    new_end_date = end_date + relativedelta(day=+day_separation,
                                            weeks=+week_separation,
                                            months=+month_separation)

    return new_start_date, new_end_date


def set_relative_occurrence_date(start_date, end_date, day_of_week, week_of_month, separation_count):
    """
    Sets the relative date interval between events

    :param start_date:
    :param end_date:
    :param month_separation:
    :param day_of_week:
    :param week_of_month:
    :param separation_count:
    :return:
    # Support for every specific interval
    # For example: Every month on the 3rd day of the 2nd week
    """
    start_end_difference = relativedelta(end_date, start_date)
    new_start_date = set_next_relative_date(start_date, day_of_week, week_of_month, separation_count)
    new_end_date = new_start_date + start_end_difference

    return new_start_date, new_end_date


def set_next_relative_date(start_date, day_of_week, week_of_month, separation_count):
    arg = MO(1)

    if day_of_week == 1:
        arg = MO(week_of_month)
    if day_of_week == 2:
        arg = TU(week_of_month)
    if day_of_week == 3:
        arg = WE(week_of_month)
    if day_of_week == 4:
        arg = TH(week_of_month)
    if day_of_week == 5:
        arg = FR(week_of_month)
    if day_of_week == 6:
        arg = SA(week_of_month)
    if day_of_week == 7:
        arg = SU(week_of_month)

    if week_of_month == -1:
        return start_date + relativedelta(day=31,
                                          months=+separation_count,
                                          weekday=arg)

    return start_date + relativedelta(day=1,
                                      months=+separation_count,
                                      weekday=arg)
