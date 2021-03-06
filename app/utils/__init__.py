from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from .error_handlers import handle_exception
from .logs import Logs

db = SQLAlchemy()


def to_camel_case(snake_str):
    """Format string to camel case."""
    title_str = snake_str.title().replace("_", "")
    return title_str[0].lower() + title_str[1:]


def to_pascal_case(word, sep="_"):
    return "".join(list(map(lambda x: x.capitalize(), word.split(sep))))


def format_response_timestamp(date_obj):
    if isinstance(date_obj, datetime):
        return {
            "isoDate": date_obj.isoformat(),
            "datePretty": date_obj,
            "datePrettyShort": date_obj.strftime("%b %d, %Y"),
        }


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


def current_time_by_zone(zone):
    # zone format: +1 or -3

    current_date = None
    if zone[0:1] == "+":
        current_date = datetime.utcnow() + timedelta(hours=int(zone[1:]))
    else:
        current_date = datetime.utcnow() - timedelta(hours=int(zone[1:]))

    return current_date


def check_date_current_vs_date_for(current_date, date_booked_for):

    if int((date_booked_for - current_date).days) >= 1:
        return False
    return True
