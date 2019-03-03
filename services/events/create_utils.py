from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from core import errors
from core.db import save_with_unique_id
from core.db.events.model import EventModel
from datetime import datetime as dt


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

    if recurrence_details['num_recurrences'] != 0:
        # Populate the occurrences list and last end date when recurrence number is specified
        last_end_date, occurrences = populate_occurrences(event_args['start_date'],
                                                          event_args['end_date'],
                                                          recurrence_details)
        event_args['end_date'] = last_end_date
        event_args['occurrences'] = occurrences

    if recurrence_details['num_recurrences'] == 0:
        end_date, occurrences = populate_occurrences_no_recur_num(event_args['start_date'],
                                                                       event_args['end_date'],
                                                                       recurrence_details)
        event_args['end_date'] = end_date  # Is this  needed?
        event_args['occurrences'] = occurrences


def set_default_recurrence_details():
    return {
        'recurrence': constants.RecurrenceType.DAILY.value,
        'num_recurrences': constants.MIN_RECURRENCE,
        'nday': constants.NDAY,
        'nweek': constants.NWEEK
    }


def populate_occurrences(start_date, end_date, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    occurrences = []

    for i in range(recurrence_details['num_recurrences']):
        curr_start_date, curr_end_date = set_occurrence_date(start_date,
                                                             end_date,
                                                             i * day_separation,
                                                             i * week_separation,
                                                             i * month_separation,
                                                             recurrence_details['nday'],
                                                             recurrence_details['nweek'])
        if start_date <= curr_start_date:
            occurrences.append(get_occurrence_entry(i + 1, curr_start_date, curr_end_date))

    return curr_end_date, occurrences


def populate_occurrences_no_recur_num(start_date, end_date, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    occurrences = []

    i = 0
    curr_start_date = start_date
    curr_end_date = dt.strptime(constants.DEFAULT_DATE, constants.EVENT_DATE_FORMAT)

    while curr_end_date <= end_date:
        curr_end_date = set_occurrence_date_no_recur_num(curr_start_date,
                                                         day_separation,
                                                         week_separation,
                                                         month_separation)
        occurrences.append(get_occurrence_entry(i + 1, curr_start_date, curr_start_date))
        curr_start_date = curr_end_date
        i += 1

    return end_date, occurrences


def get_occurrence_entry(occurrence_num, start_date, end_date):
    return {
        'occurrence_num': occurrence_num,
        'start_date': start_date,
        'end_date': end_date
    }


def set_occurrence_date(start_date, end_date, day_separation, week_separation, month_separation, nday_separation, nweek_separation):
    if (nweek_separation != 0) and (nday_separation != 0):
        arg = MO(1)
        if nday_separation == 1: arg = MO(nweek_separation)
        if nday_separation == 2: arg = TU(nweek_separation)
        if nday_separation == 3: arg = WE(nweek_separation)
        if nday_separation == 4: arg = TH(nweek_separation)
        if nday_separation == 5: arg = FR(nweek_separation)
        if nday_separation == 6: arg = SA(nweek_separation)
        if nday_separation == 7: arg = SU(nweek_separation)

        new_start_date = start_date + relativedelta(day=1,
                                                    months=+month_separation,
                                                    weekday=arg)

        new_end_date = end_date + relativedelta(day=1,
                                                months=+month_separation,
                                                weekday=arg)
    else:
        new_start_date = start_date + relativedelta(day=+day_separation,
                                                    weeks=+week_separation,
                                                    months=+month_separation)

        new_end_date = end_date + relativedelta(day=+day_separation,
                                                weeks=+week_separation,
                                                months=+month_separation)

    return new_start_date, new_end_date


def set_occurrence_date_no_recur_num(start_date, day_separation, week_separation, month_separation):

    new_end_date = start_date + relativedelta(day=+day_separation,
                                              weeks=+week_separation,
                                              months=+month_separation)

    return new_end_date


def base_daily_interval():
    return 1, 0, 0


def base_weekly_interval():
    return 0, 1, 0


def base_bi_weekly_interval():
    return 0, 2, 0


def base_monthly_interval():
    return 0, 0, 1


def base_nweekday_interval():
    return 0, 0, 1


def define_interval_increments(recurrence):
    switcher = {
        constants.RecurrenceType.DAILY.value: base_daily_interval(),
        constants.RecurrenceType.WEEKLY.value: base_weekly_interval(),
        constants.RecurrenceType.BI_WEEKLY.value: base_bi_weekly_interval(),
        constants.RecurrenceType.MONTHLY.value: base_monthly_interval(),
        constants.RecurrenceType.NWEEKDAY.value: base_nweekday_interval()

    }

    # Get the function from switcher dictionary
    return switcher.get(recurrence, lambda: "Invalid Interval Value")
