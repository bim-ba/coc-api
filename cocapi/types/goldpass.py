from typing import Any
from datetime import datetime

from pydantic import validator

from .base import DefaultBaseModel


class GoldPass(DefaultBaseModel):
    start_time: datetime
    end_time: datetime

    @validator(
        "start_time", "end_time", "preparation_start_time", pre=True, check_fields=False
    )
    def parse_datetime(cls: Any, value: Any):  # pylint: disable=no-self-argument
        if isinstance(value, str):
            fmt = "%Y%m%dT%H%M%S.%fZ"
            return datetime.strptime(value, fmt)
        return value
