import copy

from datetime import datetime
from dateutil.relativedelta import relativedelta

from core import db
from services.events import constants


# -------------------------
# Handle filter conditions
# -------------------------
def build_list_events_scan_condition(org_id):
    from core.db.events.model import EventModel

    conditions = []

    if org_id is not None:
        conditions.append(EventModel.owner == org_id)

    return db.get_filter_condition(conditions)


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
