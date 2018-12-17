import copy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from webargs import missing

from core import errors
from services.events import constants


# -------------------------
# Handle filter conditions
# -------------------------
def set_dates_filter(start_date, end_date):
    if not start_date and not end_date:
        today = datetime.today()
        filter_date = datetime(today.year, today.month, today.day)
        return filter_date, filter_date + relativedelta(days=+7)
    if start_date and not end_date:
        return start_date, start_date + relativedelta(days=+7)
    if not start_date and end_date:
        return end_date + relativedelta(days=-7), end_date

    return start_date, end_date


def set_category_filter(categories):
    category_filters = []
    if categories is not missing:
        category_filters = categories.split(',')

    return category_filters


# ------------------------------
# Handle event update actions
# ------------------------------
def build_update_actions(event, event_args):
    from core.db.events.model import EventModel

    actions = []

    # Check for changes in the recurrences
    # reset_occurrences = False
    is_recurring = event_args['is_recurring']
    if is_recurring is not missing and is_recurring != event.is_recurring:
        # reset_occurrences = True
        actions.append(EventModel.is_recurring.set(is_recurring))

    # recurrence_details = event_args['recurrence_details']
    # if recurrence_details and recurrence_details != event.recurrence_details:
    #     reset_occurrences = True
    #
    # Reset the occurrences
    # if reset_occurrences:
    set_occurrences(event_args)
    actions.append(EventModel.occurrences.set(event_args['occurrences']))

    recurrence_details = event_args['recurrence_details']
    if recurrence_details and recurrence_details != event.recurrence_details:
        actions.append(EventModel.recurrence_details.set(event_args['recurrence_details']))
    else:
        actions.append(EventModel.recurrence_details.remove())

    name = event_args['name']
    if name and name != event.name:
        actions.append(EventModel.name.set(name))

    description = event_args['description']
    if description and description != event.description:
        actions.append(EventModel.description.set(description))

    categories = event_args['categories']
    if categories and not are_lists_equal(categories, event.categories):
        actions.append(EventModel.categories.set(categories))

    start_date = event_args['start_date']
    if start_date and start_date != event.start_date:
        actions.append(EventModel.start_date.set(start_date))

    end_date = event_args['end_date']
    if end_date and end_date != event.end_date:
        actions.append(EventModel.end_date.set(end_date))

    start_time = event_args['start_time']
    if start_time and start_time != event.start_time:
        actions.append(EventModel.start_time.set(start_time))

    end_time = event_args['end_time']
    if end_time and end_time != event.end_time:
        actions.append(EventModel.end_time.set(end_time))

    return actions


def are_lists_equal(list1, list2):
    return sorted(list1) == sorted(list2)


def check_recurrence_details_changed(event, event_args):
    # is_recurring = event_args['is_recurring']
    recurrence_details = event_args['recurrence_details']
    if recurrence_details:
        print(recurrence_details['recurrence'])
        print(event.recurrence_details)
        # if recurrence_details['num_recurrences'] != event.recurrence_details.num_recurrences or \
        #         recurrence_details['recurrence'] != event.recurrence_details.recurrence:
        #     return True

    return False


# Handle change to specific occurrences
# TODO: Handle change to the time
def update_event_occurrences(event):
    # Retrieve the list of occurrences from the original event
    occurrences = event.occurrences
    from operator import itemgetter
    # new_list = sorted(occurrences, key=lambda k: k['occurrence_num'])
    new_list = sorted(occurrences, key=itemgetter('occurrence_num'))
    for occurrence in new_list:
        print(occurrence.occurrence_num)

    # Slice the list
    # from dateutil import parser
    # print('Start List')
    # print([x for x in occurrences if x.occurrence_num < 3])
    # print('Match List')
    # print([x for x in occurrences if x.occurrence_num == 3])
    # print('End List')
    # print([x for x in occurrences if x.occurrence_num > 3])

    # if update_type == 'THIS-EVENT':
    #     # Update the list of occurrences
    #
    # elif update_type == 'REMAINING-EVENTS':
    pass


# -------------------------
# Set occurrences on save
# -------------------------
def set_occurrences(event_args):
    # Check to see if the recurrence details is set
    if event_args['is_recurring']:
        recurrence_details = event_args['recurrence_details']
        if recurrence_details is missing:
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


# -------------------------
# List occurrences on read
# -------------------------
def get_recurring_events_list(event, start_date, end_date, category_filters):
    return [get_recurring_event(event, occurrence) for occurrence in event.occurrences
            if within_date_range(occurrence, start_date, end_date) and contains_category(event.categories, category_filters)]


def within_date_range(occurrence, start_date, end_date):
    return start_date <= occurrence.start_date <= end_date or \
           start_date <= occurrence.end_date <= end_date


def contains_category(categories, category_filters):
    if not category_filters:
        return True

    return True if set(categories) & set(category_filters) else False


def get_recurring_event(event, occurrence):
    # Perform a deep copy of the event object so that unique objects are inserted in the list
    new_event = copy.deepcopy(event)
    new_event.occurrence_num = occurrence.occurrence_num
    new_event.start_date = occurrence.start_date
    new_event.end_date = occurrence.end_date

    return new_event
