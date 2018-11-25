import copy
# import pendulum

from datetime import datetime
from dateutil import parser
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
        filter_date = datetime(today.year, today.month, today.day)  # .strftime('%Y-%m-%d')
        # print(filter_date + relativedelta(days=+7))
        # filter_date = pendulum.today()
        # return filter_date, filter_date.add(days=7)
        return filter_date, filter_date + relativedelta(days=+7)
    if start_date and not end_date:
        return start_date, start_date + relativedelta(days=+7)
        # filter_date = pendulum.instance(start_date)
        # return filter_date, filter_date.add(days=7)
    if not start_date and end_date:
        return end_date + relativedelta(days=-7), end_date
        # filter_date = pendulum.instance(end_date)
        # return filter_date.subtract(days=7), filter_date
    # if start_date and end_date:
    #     return pendulum.instance(start_date), pendulum.instance(end_date)

    return start_date, end_date


# -------------------------
# Set occurrences on save
# -------------------------
def set_occurrences(event_args):
    # start_date = pendulum.instance(event_args['start_date'])
    # start_date = event_args['start_date']
    # end_date = event_args['end_date']

    if event_args['is_recurring']:
        # Look for the recurrence details
        # recurrence_details = event_args['recurrence_details']
        # if recurrence_details is missing:
        #     message = 'Missing data for required field'
        #     raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

        event_args['occurrences'] = populate_occurrences(event_args)
        # occurrences, end_date = populate_occurrences(start_date, end_date, recurrence_details)
    else:
        # Populate a single occurrence
        event_args['recurrence_details'] = None
        # occurrences = [start_date.strftime(constants.EVENT_DATE_FORMAT)]
        event_args['occurrences'] = [get_occurrence_entry(1, event_args['start_date'], event_args['end_date'])]

    # Update the occurrences and end date to reflect the last occurrence
    # event_args['occurrences'] = occurrences
    # event_args['end_date'] = end_date


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


# def populate_occurrences(start_date, end_date, recurrence_details):
#     day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])
#
#     # curr_start_date = start_date
#     # last_occurrence_date = end_date
#     occurrences = []
#
#     for i in range(recurrence_details['num_recurrences']):
#         # from dateutil.relativedelta import relativedelta
#         # last_occurrence_date = start_date + relativedelta(day=i*day_separation,
#         #                                                   weeks=i*week_separation,
#         #                                                   months=i*month_separation)
#
#         curr_start_date, last_occurrence_date = set_occurrence_date(start_date,
#                                                                     end_date,
#                                                                     i * day_separation,
#                                                                     i * week_separation,
#                                                                     i * month_separation)
#         # curr_start_date = set_occurrence_date(start_date,
#         #                                       i*day_separation,
#         #                                       i*week_separation,
#         #                                       i*month_separation)
#         #
#         # last_occurrence_date = set_occurrence_date(end_date,
#         #                                            i*day_separation,
#         #                                            i*week_separation,
#         #                                            i*month_separation)
#
#         occurrences.append(get_occurrence_entry(i+1, curr_start_date, last_occurrence_date))
#         # {'occurrence_num': i+1,
#         #                     'start_date': curr_start_date,
#         #                     'end_date': last_occurrence_date})
#
#         # occurrence_num = i
#         # last_occurrence_date = start_date.add(days=i*day_separation,
#         # occurrences.update({occurrence_num: dict(start_date=curr_start_date.strftime(constants.EVENT_DATE_FORMAT),
#         #                                          end_date=last_occurrence_date.strftime(constants.EVENT_DATE_FORMAT))})
#         #                                       weeks=i*week_separation,
#         #                                       months=i*month_separation)
#
#         # occurrences.append(last_occurrence_date.strftime(constants.EVENT_DATE_FORMAT))
#
#     return occurrences, last_occurrence_date


def get_occurrence_entry(occurrence_num, start_date, end_date):
    return {
        'occurrence_num': occurrence_num,
        'start_date': start_date,
        'end_date': end_date
    }

# def populate_occurrences(start_date, recurrence_details):
#     day_separation, week_separation, month_separation = define_interval_increments(recurrence_details['recurrence'])
#
#     last_occurrence_date = start_date
#     occurrences = []
#
#     for i in range(recurrence_details['num_recurrences']):
#         # from dateutil.relativedelta import relativedelta
#         # last_occurrence_date = start_date + relativedelta(day=i*day_separation,
#         #                                                   weeks=i*week_separation,
#         #                                                   months=i*month_separation)
#
#         last_occurrence_date = set_occurrence_date(start_date,
#                                                    i*day_separation,
#                                                    i*week_separation,
#                                                    i*month_separation)
#         # last_occurrence_date = start_date.add(days=i*day_separation,
#         #                                       weeks=i*week_separation,
#         #                                       months=i*month_separation)
#         occurrences.append(last_occurrence_date.strftime(constants.EVENT_DATE_FORMAT))
#
#     return occurrences, last_occurrence_date


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
    # print(filter_end_date.int_timestamp())

    return [get_recurring_event(event, occurrence) for occurrence in event.occurrences
            if within_date_range(occurrence, start_date, end_date)]
    # occurrences = event.occurrences
    # occurrences_list = []
    # for occurrence in event.occurrences:
    #     new_event = get_recurring_event(event, occurrence)
    #
    #     if filter_start_date <= new_event.start_date <= filter_end_date or \
    #             filter_start_date <= new_event.end_date <= filter_end_date:
    #         occurrences_list.append(new_event)
    #
    # return occurrences_list
    # if occurrences:
    #     return [get_recurring_event(event, occurrence) for occurrence in occurrences]
    # else:
    #     return [event]


def within_date_range(occurrence, start_date, end_date):
    # print(occurrence.start_date)
    # date = occurrence.start_date
    # date = parser.parse(occurrence.start_date)
    # occurrence_start_date = occurrence.start_date
    # occurrence_start_date = occurrence.start_date
    # print(datetime.fromtimestamp(start_date.timestamp()))
    # print(f'Date {date}, Start Date {start_date}, End Date {end_date}')
    # date = pendulum.parse(occurrence, strict=False)
    return start_date <= occurrence.start_date <= end_date or \
           start_date <= occurrence.end_date <= end_date


def get_recurring_event(event, occurrence):
    # start_date = occurrence.start_date
    # end_date = occurrence.end_date
    # date = parser.parse(occurrence.start_date)
    # date = pendulum.parse(occurrence, strict=False)

    # Perform a deep copy of the event object so that unique objects are inserted in the list
    new_event = copy.deepcopy(event)
    new_event.start_date = occurrence.start_date
    new_event.end_date = occurrence.end_date

    return new_event

