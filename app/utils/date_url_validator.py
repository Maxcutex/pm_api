from datetime import datetime

from werkzeug.exceptions import BadRequest
from werkzeug.routing import BaseConverter, ValidationError


class DateValidator(BaseConverter):
    """Date from the path and validates it."""

    def to_python(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except Exception:
            raise BadRequest(
                "Bad Request - {} should be valid date. Format: YYYY-MM-DD".format(
                    value
                )
            )
        return value
