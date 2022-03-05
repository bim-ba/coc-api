# pyright: strict

from typing import Any

class UnknownLocationError(Exception):
    """Unknown location (it is not in `self._locations`)"""

    def __init__(self, location: Any, message: str ='Unknown location! Check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block'):
        self.location = location
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.location} -> {self.message}'

class UnknownClanLabelError(Exception):
    """Unknown clan label (it is not in `self._clan_labels`)"""

    def __init__(self, location: Any, message: str ='Unknown clan label! Check `self._clan_labels` or official API reference https://developer.clashofclans.com/#/documentation for "labels/labels/clans" block'):
        self.location = location
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.location} -> {self.message}'
