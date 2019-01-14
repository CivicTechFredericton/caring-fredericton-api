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

    name = event_args['name']
    if name and name != event.name:
        actions.append(EventModel.name.set(name))

    description = event_args['description']
    if description and description != event.description:
        actions.append(EventModel.description.set(description))

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

    is_recurring = event_args['is_recurring']
    if is_recurring and is_recurring != event.is_recurring:
        actions.append(EventModel.is_recurring.set(is_recurring))
        # insert new recurrences since this option was not enabled
        set_occurrences(event_args)
        # TODO 
        # is_recurring = false, cancel the actual recurrence or the remaining recurrences, think about
        # is_recurring = true, create new recurrences if doesn't exist any
        # if recurrences_details changed:
        # what changes could be? 
        # 1- change a single reccurence
        # 2- change everything starting from a specefic reccurence
        # 3- cancel one or more reccurences
        # 4- cancel all starting from a specefic reccurence
    elif not is_recurring and is_recurring != event.is_recurring:
        actions.append(EventModel.is_recurring.set(is_recurring))
        # cancel the remaining events 
        today = datetime.now()
        recurrence_details = event.recurrence_details
        num_recurrences = recurrence_details.num_recurrences
        occurrenses = event.occurrences
        for occurrence in occurrenses:
            if occurrence.start_date >= today:
                occurrence.is_still_on = False

        actions.append(EventModel.occurrences.set(occurrences))

    elif is_recurring and is_recurring == event.is_recurring:
        # check for reccurrences changes  
        recurrence_details = event_args['recurrence_details']
        # check for occurrenses changes
        occurrences = event_args['occurrences']

        actions.append(EventModel.recurrence_details.set(recurrence_details))
        actions.append(EventModel.occurrences.set(occurrences))
    elif not is_recurring and is_recurring == event.is_recurring:
        # do nothing
        pass

    # TODO: Handle recurrences
    # recurrences 

    return actions


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
    new_event.start_date = occurrence.start_date
    new_event.end_date = occurrence.end_date

    return new_event
