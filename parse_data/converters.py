import re
from datetime import datetime
from decimal import Decimal


def date_value(value):
    if re.match("^[0-9]{2}:[0-9]{2}$", value):
        return datetime.now().date()
    return datetime.strptime(value, "%m/%d/%Y").date()


def dec_value(value):
    return Decimal(value)


def sum_value(value: str):
    return int(value.replace(",", ""))
