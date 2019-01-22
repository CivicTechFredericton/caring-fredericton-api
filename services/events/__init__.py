import copy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter

from core import db, errors
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
    if categories:
        category_filters = categories.split(',')

    return category_filters


# ------------------------------
# Event retrieval actions
# ------------------------------
def get_event_occurrence(event, occurrence_num):
    occurrences = event.occurrences
    occurrence = next((x for x in occurrences if x.occurrence_num == occurrence_num), None)
    return get_recurring_event(event, occurrence) if occurrence else None


# ------------------------------
# Handle event update actions
# ------------------------------
def build_update_actions(event, event_args):
    from core.db.events.model import EventModel

    actions = []

    # Check for changes in the recurrences
    reset_occurrences, is_recurring_changed = check_recurrence_details_changed(event, event_args)
    if is_recurring_changed:
        actions.append(EventModel.is_recurring.set(event_args['is_recurring']))

    if reset_occurrences:
        # Reset the occurrences
        set_occurrences(event_args)
        actions.append(EventModel.occurrences.set(event_args['occurrences']))

        # Check the updated recurrence details
        recurrence_details = event_args.get('recurrence_details')
        if recurrence_details is not None:
            actions.append(EventModel.recurrence_details.set(recurrence_details))
        else:
            actions.append(EventModel.recurrence_details.remove())

    # Check the remainder of the attributes
    name = event_args.get('name')
    if name and name != event.name:
        actions.append(EventModel.name.set(name))

    description = event_args.get('description')
    if description and description != event.description:
        actions.append(EventModel.description.set(description))

    categories = event_args.get('categories')
    if categories and not are_lists_equal(categories, event.categories):
        actions.append(EventModel.categories.set(categories))

    # TODO: Work with the occurrence record
    start_date = event_args.get('start_date')
    if start_date and start_date != event.start_date:
        actions.append(EventModel.start_date.set(start_date))

    end_date = event_args.get('end_date')
    if end_date and end_date != event.end_date:
        actions.append(EventModel.end_date.set(end_date))

    start_time = event_args.get('start_time')
    if start_time and start_time != event.start_time:
        actions.append(EventModel.start_time.set(start_time))

    end_time = event_args.get('end_time')
    if end_time and end_time != event.end_time:
        actions.append(EventModel.end_time.set(end_time))

    return actions


def check_recurrence_details_changed(event, event_args):
    # Check for changes in the recurrences
    reset_occurrences = False
    is_recurring_changed = False

    is_recurring = event_args.get('is_recurring')
    if is_recurring is not None and is_recurring != event.is_recurring:
        reset_occurrences = True
        is_recurring_changed = True
    else:
        event_args['is_recurring'] = event.is_recurring

    # Check to see if the details changed
    recurrence_details = event_args.get('recurrence_details')
    if recurrence_details and recurrence_details != event.recurrence_details:
        reset_occurrences = True

    return reset_occurrences, is_recurring_changed


def are_lists_equal(list1, list2):
    return sorted(list1) == sorted(list2)


# Handle change to specific occurrences
# TODO: Handle change to the time
def update_event_occurrences(event, event_args):
    update_details = event_args.get('update_details')
    if update_details is None:
        message = 'Missing update_details values'
        raise errors.ResourceValidationError(messages={'update_details': [message]})

    occurrence_num = update_details['occurrence_num']

    update_type = update_details['update_type']
    if update_type == constants.UpdateType.ALL.value:
        actions = build_update_actions(event, event_args)
        db.update_item(event, actions)

    # TODO: Link together separated models
    if update_type == constants.UpdateType.ONE_TIME.value:
        actions = get_original_event_actions(event, occurrence_num)
        db.update_item(event, actions)

        # Create a new record with the one time recurrence
        # TODO: Populate with original model values and adjust based on optional arguments
        event_args['is_recurring'] = False
        create_event(**event_args)

        # Create a new record with original details and remaining recurrences
        remaining_events_args = get_remaining_events_arguments(event, occurrence_num)
        create_event(**remaining_events_args)

    if update_type == constants.UpdateType.REMAINING.value:
        actions = get_original_event_actions(event, occurrence_num)
        db.update_item(event, actions)

        remaining_events_args = get_remaining_events_arguments(event, occurrence_num)
        create_event(**remaining_events_args)


def get_original_event_actions(event, occurrence_num):
    """
    Adjust the original record to end prior to the specified occurrence
    :param event:
    :param occurrence_num:
    :return:
    """
    update_event_args = {}

    occurrences = event.occurrences
    original_events = sorted([x for x in occurrences if x.occurrence_num < occurrence_num],
                             key=itemgetter('occurrence_num'))
    if original_events:
        original_start_occurrence = original_events[0]
        update_event_args['start_date'] = original_start_occurrence.start_date
        update_event_args['end_date'] = original_start_occurrence.end_date

        set_recurrence_details(update_event_args, len(original_events), event.recurrence_details.recurrence)

    return build_update_actions(event, update_event_args)


def get_remaining_events_arguments(event, occurrence_num):
    remaining_events_args = {}

    occurrences = event.occurrences
    remaining_events = [x for x in occurrences if x.occurrence_num > occurrence_num]
    if remaining_events:
        start_remaining_occurrence = remaining_events[0]
        # TODO: Build argument list from model
        remaining_events_args['owner'] = event.owner
        remaining_events_args['name'] = event.name
        remaining_events_args['description'] = event.description
        remaining_events_args['categories'] = event.categories
        remaining_events_args['start_date'] = start_remaining_occurrence.start_date
        remaining_events_args['end_date'] = start_remaining_occurrence.end_date
        remaining_events_args['start_time'] = event.start_time
        remaining_events_args['end_time'] = event.end_time

        set_recurrence_details(remaining_events_args, len(remaining_events), event.recurrence_details.recurrence)

    return remaining_events_args


def set_recurrence_details(event_args, num_recurrences, original_recurrence_value):
    if num_recurrences == 1:
        event_args['is_recurring'] = False
    else:
        event_args['is_recurring'] = True
        event_args['recurrence_details'] = {
            'recurrence': original_recurrence_value,
            'num_recurrences': num_recurrences
        }


# -------------------------
# Event creation
# -------------------------
def create_event(**event_args):
    # Set the number of occurrences
    set_occurrences(event_args)

    # Save the object
    from core.db.events.model import EventModel
    event = EventModel(**event_args)
    db.save_with_unique_id(event)

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


# -------------------------
# List occurrences on read
# -------------------------
def get_recurring_events_list(event, start_date, end_date, category_filters):
    return [get_recurring_event(event, occurrence) for occurrence in event.occurrences
            if within_date_range(occurrence, start_date, end_date)
            and contains_category(event.categories, category_filters)]


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
