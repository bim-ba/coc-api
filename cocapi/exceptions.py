from typing import Any, Optional

from aiohttp import ClientResponse


class ClientRequestError(Exception):
    """Error while making request"""

    response: ClientResponse
    message: str
    data: Any

    MESSAGE = "Error while making request! Server returned {status_code} for {url}. Check ``data`` for additional details!"

    def __init__(
        self,
        response: ClientResponse,
        *,
        data: Optional[Any] = None,
    ):
        self.response = response
        self.message = self.MESSAGE.format(
            status_code=response.status, url=response.url
        )
        self.data = data

        super().__init__(self.message)


class JSONContentTypeError(Exception):
    """Error while decoding json"""

    content_type: str
    message: str

    MESSAGE = "aiohttp throws an error while decoding JSON from the request! Content type was {content_type}: {error}"

    def __init__(self, content_type: str, error: Any):
        self.content_type = content_type
        self.message = self.MESSAGE.format(content_type=content_type, error=error)
        super().__init__(self.message)


class UnknownLocationError(Exception):
    """Unknown location (it is not in `self._locations`)"""

    location: Any
    message: str

    MESSAGE = 'Unknown location! To get available locations, check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block'

    def __init__(self, location: Any):
        self.location = location
        self.message = self.MESSAGE
        super().__init__(self.message)

    def __str__(self):
        return f"{self.location} -> {self.message}"


class UnknownClanLabelError(Exception):
    """Unknown clan label (it is not in `self._clan_labels`)"""

    clan_label: Any
    message: str

    MESSAGE = 'Unknown clan label! To get available clan labels, check `self._clan_labels` or official API reference https://developer.clashofclans.com/#/documentation for "labels/labels/clans" block'

    def __init__(self, clan_label: Any):
        self.clan_label = clan_label
        self.message = self.MESSAGE
        super().__init__(self.message)

    def __str__(self):
        return f"{self.clan_label} -> {self.message}"
