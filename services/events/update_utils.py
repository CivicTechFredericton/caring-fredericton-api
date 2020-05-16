# from operator import itemgetter

# from core import errors
# from core.db import update_item
from core.db.events.model import EventModel
# from services.events import constants
# from services.events.create_utils import set_occurrences # This is deprecated, below the new functions
# from services.events.create_utils_bak import set_occurrences_one_time, set_occurrences_recurring_ending, set_occurrences_recurring_not_ending


# ------------------------------
# Handle event update actions
# ------------------------------
def build_update_actions(event, event_args):
    actions = []

    # Check the remainder of the attributes
    name = event_args.get('name')
    if name and name != event.name:
        actions.append(EventModel.name.set(name))

    description = event_args.get('description')
    if description and description != event.description:
        actions.append(EventModel.description.set(description))

    contact_email = event_args.get('contact_email')
    if contact_email and contact_email != event.contact_email:
        actions.append(EventModel.contact_email.set(contact_email))

    location = event_args.get('location')
    if location and location != event.location:
        actions.append(EventModel.location.set(location))

    categories = event_args.get('categories')
    if categories and not are_lists_equal(categories, event.categories):
        actions.append(EventModel.categories.set(categories))

    # TODO: Only update the start date and end date for the occurrence
    # start_date = event_args.get('start_date')
    # if start_date and start_date != event.start_date:
    #     actions.append(EventModel.start_date.set(start_date))
    #
    # end_date = event_args.get('end_date')
    # if end_date and end_date != event.end_date:
    #     actions.append(EventModel.end_date.set(end_date))

    # start_time = event_args.get('start_time')
    # if start_time and start_time != event.start_time:
    #     actions.append(EventModel.start_time.set(start_time))
    #
    # end_time = event_args.get('end_time')
    # if end_time and end_time != event.end_time:
    #     actions.append(EventModel.end_time.set(end_time))

    # Check for changes in the recurrences
    # reset_occurrences, is_recurring_changed = check_recurrence_details_changed(event, event_args)
    # if is_recurring_changed:
    #     actions.append(EventModel.is_recurring.set(event_args['is_recurring']))
    #
    # if reset_occurrences:
    #     # Reset the occurrences
    #     # set_occurrences(event_args)
    #     actions.append(EventModel.occurrences.set(event_args['occurrences']))
    #
    #     # Check the updated recurrence details
    #     recurrence_details = event_args.get('recurrence_details')
    #     if recurrence_details is not None:
    #         actions.append(EventModel.recurrence_details.set(recurrence_details))
    #     else:
    #         actions.append(EventModel.recurrence_details.remove())

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

    # Check to see if the start or end time has changed

    return reset_occurrences, is_recurring_changed


def are_lists_equal(list1, list2):
    return sorted(list1) == sorted(list2)


# Handle change to specific occurrences
# TODO: Uncomment when pattern is resolved
# def update_event_occurrences(event, event_args):
#     update_details = event_args.get('update_details')
#     if update_details is None:
#         message = 'Missing update_details values'
#         raise errors.ResourceValidationError(messages={'update_details': [message]})
#
#     occurrence_num = update_details['occurrence_num']
#
#     update_type = update_details['update_type']
#     if update_type == constants.UpdateType.ALL.value:
#         actions = build_update_actions(event, event_args)
#         update_item(event, actions)
#
#     # TODO: Link together separated models
#     if update_type == constants.UpdateType.ONE_TIME.value:
#         actions = get_original_event_actions(event, occurrence_num)
#         db.update_item(event, actions)
#
#         # Create a new record with the one time recurrence
#         # TODO: Populate with original model values and adjust based on optional arguments
#         event_args['is_recurring'] = False
#         create_event(**event_args)
#
#         # Create a new record with original details and remaining recurrences
#         remaining_events_args = get_remaining_events_arguments(event, occurrence_num)
#         create_event(**remaining_events_args)
#
#     if update_type == constants.UpdateType.REMAINING.value:
#         actions = get_original_event_actions(event, occurrence_num)
#         db.update_item(event, actions)
#
#         remaining_events_args = get_remaining_events_arguments(event, occurrence_num)
#         create_event(**remaining_events_args)
#
#
# def get_original_event_actions(event, occurrence_num):
#     """
#     Adjust the original record to end prior to the specified occurrence
#     :param event:
#     :param occurrence_num:
#     :return:
#     """
#     update_event_args = {}
#
#     occurrences = event.occurrences
#     original_events = sorted([x for x in occurrences if x.occurrence_num < occurrence_num],
#                              key=itemgetter('occurrence_num'))
#     if original_events:
#         original_start_occurrence = original_events[0]
#         update_event_args['start_date'] = original_start_occurrence.start_date
#         update_event_args['end_date'] = original_start_occurrence.end_date
#
#         set_recurrence_details(update_event_args, len(original_events), event.recurrence_details.recurrence)
#
#     return build_update_actions(event, update_event_args)
#
#
# def get_remaining_events_arguments(event, occurrence_num):
#     remaining_events_args = {}
#
#     occurrences = event.occurrences
#     remaining_events = [x for x in occurrences if x.occurrence_num > occurrence_num]
#     if remaining_events:
#         start_remaining_occurrence = remaining_events[0]
#         # TODO: Build argument list from model
#         remaining_events_args['owner'] = event.owner
#         remaining_events_args['name'] = event.name
#         remaining_events_args['description'] = event.description
#         remaining_events_args['categories'] = event.categories
#         remaining_events_args['start_date'] = start_remaining_occurrence.start_date
#         remaining_events_args['end_date'] = start_remaining_occurrence.end_date
#         remaining_events_args['start_time'] = event.start_time
#         remaining_events_args['end_time'] = event.end_time
#
#         set_recurrence_details(remaining_events_args, len(remaining_events), event.recurrence_details.recurrence)
#
#     return remaining_events_args
#
#
# def set_recurrence_details(event_args, num_recurrences, original_recurrence_value):
#     if num_recurrences == 1:
#         event_args['is_recurring'] = False
#     else:
#         event_args['is_recurring'] = True
#         event_args['recurrence_details'] = {
#             'recurrence': original_recurrence_value,
#             'num_recurrences': num_recurrences
#         }
