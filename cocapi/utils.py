from typing import Text
from datetime import datetime

from .aliases import Tag


def rawtime_to_datetime(date_string: Text):
    fmt = "%Y%m%dT%H%M%S.%fZ"
    try:
        time = datetime.strptime(date_string, fmt)
        return time
    except ValueError:
        return date_string


def shape_tag(tag: Tag):
    true_tag = tag.upper()

    if not true_tag.startswith("#"):
        true_tag = f"#{true_tag}"

    return true_tag.replace("#", "%23")
