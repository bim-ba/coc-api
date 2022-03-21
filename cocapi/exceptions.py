from typing import Any


class UnknownLocationError(Exception):
    """Unknown location (it is not in `self._locations`)"""

    location: Any
    message: str

    def __init__(
        self,
        location: Any,
        message: str = 'Unknown location! To get available locations, check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block',
    ):
        self.location = location
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.location} -> {self.message}"


class UnknownClanLabelError(Exception):
    """Unknown clan label (it is not in `self._clan_labels`)"""

    label: Any
    message: str

    def __init__(
        self,
        clan_label: Any,
        message: str = 'Unknown clan label! To get available clan labels, check `self._clan_labels` or official API reference https://developer.clashofclans.com/#/documentation for "labels/labels/clans" block',
    ):
        self.clan_label = clan_label
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.clan_label} -> {self.message}"
