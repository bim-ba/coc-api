from typing import Optional

from .base import DefaultBaseModel
from .aliases import CaseInsensitiveStr
from .badges import BadgeURLs


class BaseLabel(DefaultBaseModel, anystr_lower=True):
    id: int
    name: CaseInsensitiveStr
    icon_urls: BadgeURLs


class BaseLeague(DefaultBaseModel, anystr_lower=True):
    id: int
    name: CaseInsensitiveStr
    icon_urls: Optional[BadgeURLs]
