#!/usr/bin/env python
import datetime
import calendar


def LastThInMonth(year, month):
    # Create a datetime.date for the last day of the given month
    first_day_of_month, days_in_month = calendar.monthrange(year, month)
    dt = datetime.date(year, month, days_in_month)

    # Back up to the most recent Thursday
    offset = 4 - dt.isoweekday()
    if offset > 0:
        offset -= 7                          # Back up one week if necessary
    dt += datetime.timedelta(offset)                    # dt is now date of last Th in month

    # Throw an exception if dt is in the current month and occurred before today
    now = datetime.date.today()                         # Get current date (local time, not utc)
    if dt.year == now.year and dt.month == now.month and dt < now:
        raise Exception('Oops - missed the last Thursday of this month')

    return dt


def set_day_of_month(year, month, week_num, day_number):
    first_day_of_month, days_in_month = calendar.monthrange(year, month)
    dt = datetime.date(year, month, days_in_month)

    offset = day_number - dt.isoweekday()
    if offset > 0:
        offset -= 7  # Back up one week if necessary
    dt += datetime.timedelta(offset)

    return dt


for month in range(1, 13):
    # print(LastThInMonth(2019, month))
    print(set_day_of_month(2019, month, 2, 3))
# for month in range(1, 13): print(set_day_of_month(2019, month, 2, 3))
