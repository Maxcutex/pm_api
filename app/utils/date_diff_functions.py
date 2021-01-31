import datetime
from dateutil import relativedelta


def date_diff_string(start_date, end_date):
    diff = relativedelta.relativedelta(end_date, start_date)
    date_diff = ""
    if diff.years > 0:
        date_diff += "{} yrs ".format(diff.years)
    if diff.months > 0:
        date_diff += "{} mon ".format(diff.months)

    # years = diff.years
    # months = diff.months
    # days = diff.days

    # print("{} yrs {} months {} days".format(years, months, days))

    return date_diff
