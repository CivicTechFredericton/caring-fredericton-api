import pendulum

from core import errors
from services.events import constants
from webargs import missing


def set_occurrences(event_args):
    if event_args['is_recurring']:
        # Look for the recurrence details
        recurrence_details = event_args['recurrence_details']
        if recurrence_details is missing:
            message = 'Missing data for required field'
            raise errors.ResourceValidationError(messages={'recurrence_details': [message]})

        start_date = pendulum.instance(event_args['start_date'])
        occurrences, new_end_date = populate_occurrences(start_date, recurrence_details)
        # num_recurrences = recurrence_details['num_recurrences']

        # occurrences = []
        # recurrence = recurrence_details['recurrence']
        # if recurrence == constants.RecurrenceType.DAILY.value:
        #     occurrences = [add_day_to_date(start_date, i) for i in range(num_recurrences)]
        #     # occurrences, new_end_date = zip(*(add_day_to_date(start_date, i) for i in range(num_recurrences)))
        #     # occurrences, new_end_date = populate_occurrences(start_date, recurrence_details)
        # if recurrence == constants.RecurrenceType.WEEKLY.value:
        #     occurrences = [add_week_to_date(start_date, i) for i in range(num_recurrences)]
        #     # occurrences, new_end_date = populate_occurrences(start_date, recurrence_details)
        #     # occurrences, new_end_date = zip(*(add_week_to_date(start_date, i) for i in range(num_recurrences)))
        # if recurrence == constants.RecurrenceType.BI_WEEKLY.value:
        #     occurrences = [add_week_to_date(start_date, i*2) for i in range(num_recurrences)]
        #     # occurrences, new_end_date = zip(*(add_week_to_date(start_date, i*2) for i in range(num_recurrences)))
        # if recurrence == constants.RecurrenceType.MONTHLY.value:
        #     occurrences = [add_month_to_date(start_date, i) for i in range(num_recurrences)]
        #     # occurrences, new_end_date = zip(*(add_month_to_date(start_date, i) for i in range(num_recurrences)))

        event_args['occurrences'] = occurrences

        # Update the end date to reflect the last occurrence
        # new_end_date = pendulum.parse(occurrences[-1])
        event_args['end_date'] = pendulum.instance(new_end_date)


def populate_occurrences(start_date, recurrence_details):
    # start_date = pendulum.instance(event_args['start_date'])

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

    # method_name = 'base_{}_interval'.format(str(recurrence).lower())
    # Get the method from 'self'. Default to a lambda.
    # return getattr(lambda: {}, method_name, lambda: "Invalid Interval Value")


    # if recurrence == constants.RecurrenceType.DAILY.value:
    #     day_separation = 1
    #     week_separation = 0
    #     month_separation = 0
    # if recurrence == constants.RecurrenceType.WEEKLY.value:
    #     day_separation = 0
    #     week_separation = 1
    #     month_separation = 0
    # if recurrence == constants.RecurrenceType.BI_WEEKLY.value:
    #     day_separation = 0
    #     week_separation = 2
    #     month_separation = 0
    # if recurrence == constants.RecurrenceType.MONTHLY.value:
    #     day_separation = 0
    #     week_separation = 0
    #     month_separation = 1
    #
    # return day_separation, week_separation, month_separation


# def add_day(date, num_recurrences):
#     last_occurrence_date = date
#     occurrences = []
#     for i in range(num_recurrences):
#         last_occurrence_date = date.add(days=i, weeks=0, months=0)
#         occurrences.append(last_occurrence_date.strftime(constants.EVENT_DATE_FORMAT))
#
#     return occurrences, last_occurrence_date
#
#
# def add_day_to_date(date, num_days):
#     date = date.add(days=num_days)
#     return date.strftime(constants.EVENT_DATE_FORMAT)
#
#
# def add_week_to_date(date, num_weeks):
#     date = date.add(weeks=num_weeks)
#     return date.strftime(constants.EVENT_DATE_FORMAT)


# def add_month_to_date(date, num_months):
#     date = date.add(months=num_months)
#     return date.strftime(constants.EVENT_DATE_FORMAT)
