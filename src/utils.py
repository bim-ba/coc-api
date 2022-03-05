# pyright: strict

from datetime import datetime
from .aliases import Tag

def rawtime_to_datetime(raw_data: str):
    fmt = '%Y%m%dT%H%M%S.%fZ'
    time = datetime.strptime(raw_data, fmt)
    return time

def shape_tag(tag: Tag):
    return f'%23{tag[1:]}'
    