from typing import Optional


from .aliases import Url
from .base import DefaultBaseModel


class BadgeURLs(DefaultBaseModel):
    small: Url
    medium: Url
    large: Optional[Url]
