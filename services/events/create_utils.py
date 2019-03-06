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

    # Check if it is recurring but not for ever [is_recurring=True and is_ending=True ]
    if event_args['is_recurring'] and event_args['is_ending']:
        set_occurrences_recurring_ending(event_args)

    # Check if it is one time only, so not recurring and not for ever [is_recurring=False and is_ending=True ]
    if not event_args['is_recurring'] and event_args['is_ending']:
        set_occurrences_one_time(event_args)

    # Check if it is recurring and will go for ever [is_recurring=True and is_ending=False ]
    if not event_args['is_ending'] and event_args['is_recurring']:
        set_occurrences_recurring_not_ending(event_args)

    # Save the object
    event = EventModel(**event_args)
    save_with_unique_id(event)

    return event


# -------------------------
# Set occurrences on save
# -------------------------
def set_occurrences_recurring_ending(event_args):
    recurrence_details = event_args.get('recurrence_details')
    if recurrence_details is None:
        message = 'Missing data for required field when is_recurring is true'
        raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

    if recurrence_details['num_recurrences'] != 0:
        # Populate the occurrences list and last end date when recurrence number is specified
        last_end_date, occurrences = populate_occurrences(event_args['start_date'],
                                                          event_args['end_date'],
                                                          recurrence_details)
        event_args['end_date'] = last_end_date
        event_args['occurrences'] = occurrences

    if recurrence_details['num_recurrences'] == 0:
        last_end_date, occurrences = populate_occurrences_no_recur_num(event_args['start_date'],
                                                                       event_args['end_date'],
                                                                       event_args['end_date_no_recur'],
                                                                       recurrence_details)
        event_args['end_date'] = last_end_date
        event_args['occurrences'] = occurrences


def set_occurrences_recurring_not_ending(event_args):
    recurrence_details = event_args.get('recurrence_details')
    if recurrence_details is None:
        message = 'Missing data for required field when is_recurring is true'
        raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

    recurrence_details = event_args.get('recurrence_details')
    # Now populate occurrences
    last_end_date, occurrences = populate_occurrences_for_ever(event_args['start_date'],
                                                               event_args['end_date'],
                                                               recurrence_details)
    event_args['end_date'] = last_end_date
    event_args['occurrences'] = occurrences


def set_occurrences_one_time(event_args):
    recurrence_details = {
        'recurrence': constants.RecurrenceType.DAILY.value,
        'num_recurrences': constants.SINGLE_RECURRENCE,
        'nday': constants.NDAY,
        'nweek': constants.NWEEK
    }
    # Populate the occurrence and last end date
    last_end_date, occurrences = populate_occurrences(event_args['start_date'],
                                                      event_args['end_date'],
                                                      recurrence_details)

    event_args['end_date'] = last_end_date
    event_args['occurrences'] = occurrences


def populate_occurrences(start_date, end_date, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    occurrences = []
    skip_regular_occ__flag = False

    for i in range(recurrence_details['num_recurrences']):
        # Insert first occurrence as user sets and then the rest as calculated later
        if i == 0:
            occurrences.append(get_occurrence_entry(i + 1, start_date, end_date))
            # After the first event as set by the user, calculate next occurrence and add it
            curr_start_date, curr_end_date = set_occurrence_date(start_date,
                                                                 end_date,
                                                                 i * day_separation,
                                                                 i * week_separation,
                                                                 i * month_separation,
                                                                 recurrence_details['nday'],
                                                                 recurrence_details['nweek'])

            # This can happen only at the second occ calculation due to date calculated being before the start_date
            # as month is 0 and month taken into account by relativedelta before day,
            # so it begins at day1 from month of start date and adds whatever resulting possibly in date < start_date
            if start_date < curr_start_date:
                occurrences.append(get_occurrence_entry(i + 2, curr_start_date, curr_end_date))
                skip_regular_occ__flag = True

        # Check in case there is only one recurr so it needs to stop above
        if recurrence_details['num_recurrences'] > 1 and i > 0:  # otherwise, if only one recurr, we have put it already
            curr_start_date, curr_end_date = set_occurrence_date(start_date,
                                                                 end_date,
                                                                 i * day_separation,
                                                                 i * week_separation,
                                                                 i * month_separation,
                                                                 recurrence_details['nday'],
                                                                 recurrence_details['nweek'])

            if skip_regular_occ__flag is False and i < recurrence_details['num_recurrences']:
                occurrences.append(get_occurrence_entry(i + 1, curr_start_date, curr_end_date))

            if skip_regular_occ__flag is True and (i+1) < recurrence_details['num_recurrences']:
                occurrences.append(get_occurrence_entry(i + 2, curr_start_date, curr_end_date))

    return curr_end_date, occurrences


def populate_occurrences_no_recur_num(start_date, end_date, end_date_no_recur, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    occurrences = []

    i = 1
    # Add the first occ as set by the user, then the rest up to the end_date_no_recur
    occurrences.append(get_occurrence_entry(i, start_date, end_date))

    curr_start_date = start_date
    start_end_difference = relativedelta(end_date, start_date)

    while curr_start_date < end_date_no_recur:
        curr_start_date = set_occurrence_date_no_recur_num(curr_start_date,
                                                           day_separation,
                                                           week_separation,
                                                           month_separation)
        # Following if statement needed for the case the last date passes the end_date and should not be registered
        if curr_start_date < end_date_no_recur:
            occurrences.append(get_occurrence_entry(i + 1, curr_start_date, curr_start_date + start_end_difference))

        i += 1

    curr_end_date = curr_start_date + start_end_difference
    return curr_end_date, occurrences


# The simplest of calendar functions, just start_date and end_date of an event and repeats for ever in the frequency set
def populate_occurrences_for_ever(start_date, end_date, recurrence_details):
    day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])

    occurrences = []

    i = 0

    curr_start_date = start_date
    start_end_difference = relativedelta(end_date, start_date)
    # Add the first occ as set by the user, then the rest up to the MAX_RECURRENCE number
    occurrences.append(get_occurrence_entry(i + 1, curr_start_date, end_date))#curr_start_date + start_end_difference))

    while i+1 < constants.MAX_RECURRENCE:
        curr_start_date = set_occurrence_date_no_recur_num(curr_start_date,
                                                           day_separation,
                                                           week_separation,
                                                           month_separation)

        occurrences.append(get_occurrence_entry(i + 2, curr_start_date, curr_start_date + start_end_difference))

        i += 1

    curr_end_date = curr_start_date + start_end_difference
    return curr_end_date, occurrences


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

        if nweek_separation != -1:
            new_start_date = start_date + relativedelta(day=1,
                                                        months=+month_separation,
                                                        weekday=arg)
        if nweek_separation == -1:
            new_start_date = start_date + relativedelta(day=31,
                                                        months=+month_separation,
                                                        weekday=arg)

        new_end_date = new_start_date + relativedelta(end_date, start_date)
    else:
        new_start_date = start_date + relativedelta(day=+day_separation,
                                                    weeks=+week_separation,
                                                    months=+month_separation)

        new_end_date = end_date + relativedelta(day=+day_separation,
                                                weeks=+week_separation,
                                                months=+month_separation)

    return new_start_date, new_end_date


def set_occurrence_date_no_recur_num(start_date, day_separation, week_separation, month_separation):

    new_start_date = start_date + relativedelta(day=+day_separation,
                                                weeks=+week_separation,
                                                months=+month_separation)

    return new_start_date


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
