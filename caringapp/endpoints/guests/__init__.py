from caringapp.db import get_filter_condition
from caringapp.db.events.model import EventModel


def build_list_events_scan_condition(org_id):
    conditions = []

    if org_id is not None:
        conditions.append(EventModel.owner == org_id)

    return get_filter_condition(conditions)
