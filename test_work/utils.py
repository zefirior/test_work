import datetime
import decimal
from flask import json
from webargs import fields, validate


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        elif isinstance(o, decimal.Decimal):
            return str(o)

        return super().default(o)


date_field = fields.Str(
    required=True,
    validate=validate.Regexp("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
)


def strptime_or_none(date_string):
    if date_string:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return
