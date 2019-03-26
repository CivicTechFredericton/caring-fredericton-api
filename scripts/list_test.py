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


def set_day_of_month(year, month, week, day):
    # first_day_of_month, days_in_month = calendar.monthrange(year, month_num)
    # print(first_day_of_month)
    # print(days_in_month)
    dt = datetime.date(year, month, 1)
    #print(dt_first)
    # dt = datetime.date(year, month_num, days_in_month)
    #print(dt)

    offset = day - dt.isoweekday()
    if offset > 0:
        offset -= 7  # Back up one week if necessary

    # Move up specified number of weeks
    offset += week * 7
    dt += datetime.timedelta(offset)

    return dt


def set_date(year, month, week, day):
    first_day_of_month, days_in_month = calendar.monthrange(year, month)
    dt = datetime.date(year, month, days_in_month)

    offset = day - dt.isoweekday()
    if offset > 0:
        offset -= 7  # Back up one week if necessary

    # Move back specified number of weeks
    offset -= week * 7
    dt += datetime.timedelta(offset)

    return dt


def set_next_relative_date(start_date, day_of_week, week_of_month, separation_count):
    from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
    arg = MO(1)

    if day_of_week == 1:
        arg = MO(week_of_month)
    if day_of_week == 2:
        arg = TU(week_of_month)
    if day_of_week == 3:
        arg = WE(week_of_month)
    if day_of_week == 4:
        arg = TH(week_of_month)
    if day_of_week == 5:
        arg = FR(week_of_month)
    if day_of_week == 6:
        arg = SA(week_of_month)
    if day_of_week == 7:
        arg = SU(week_of_month)

    if week_of_month == -1:
        return start_date + relativedelta(day=31,
                                          months=+separation_count,
                                          weekday=arg)

    return start_date + relativedelta(day=1,
                                      months=+separation_count,
                                      weekday=arg)


for month_num in range(1, 13):
    # print(LastThInMonth(2019, month))
    print('From Start: {}'.format(set_day_of_month(2019, month_num, 1, 5)))
    print('From Start: {}'.format(set_day_of_month(2019, month_num, 1, 8)))
    # print('From End: {}'.format(set_date(2019, month_num, 1, 5)))
    # print('From End: {}'.format(set_date(2019, month_num, 1, 5)))
    # print(datetime.date(2019, month_num, 1))
    # print(set_next_relative_date(dt, 1, 5, 1))
    # print(set_day_of_month(2019, month, 1, 5))
    # set_day_of_month(2019, month, 1, 5)
# for month in range(1, 13): print(set_day_of_month(2019, month, 2, 3))
