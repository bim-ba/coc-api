from typing import Optional

from .base import DefaultBaseModel
from .aliases import CaseInsensitiveStr


class Location(DefaultBaseModel, anystr_lower=True):
    id: int
    is_country: bool
    name: CaseInsensitiveStr
    country_code: Optional[CaseInsensitiveStr]
