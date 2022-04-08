from typing import Any, Optional

import aiohttp


class ClientRequestError(Exception):
    """
    According to the official Clash of Clans API
    --------------------------------------------
    - ``400`` Client provided incorrect parameters for the request.
    - ``403`` Access denied, either because of missing/incorrect credentials or used API token does not grant access to the requested resource.
    - ``404`` Resource was not found.
    - ``429`` Request was throttled, because amount of requests was above the threshold defined for the used API token.
    - ``500`` Unknown error happened when handling the request.
    - ``503`` Service is temprorarily unavailable because of maintenance.
    """

    response: aiohttp.ClientResponse
    message: str
    data: Any | None

    MESSAGE = "Error while making request! Server returned {status_code} for {url}. Check ``data`` for additional details!"
    CODE: int | None = None
    DETAILS: str | None = None

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        *,
        data: Optional[Any] = None,
    ):
        self.response = response
        self.message = (
            self.DETAILS
            if self.DETAILS
            else self.MESSAGE.format(status_code=response.status, url=response.url)
        )
        self.data = data

        super().__init__(self.message)


class IncorrectParameters(ClientRequestError):
    CODE = 400
    DETAILS = "Client provided incorrect parameters for the request"


class AccessDenied(ClientRequestError):
    CODE = 403
    DETAILS = "Access denied, either because of missing/incorrect credentials or used API token does not grant access to the requested resource"


class ResourceNotFound(ClientRequestError):
    CODE = 404
    DETAILS = "Resource was not found"


class TooManyRequests(ClientRequestError):
    CODE = 429
    DETAILS = "Request was throttled, because amount of requests was above the threshold defined for the used API token"


class UnknownError(ClientRequestError):
    CODE = 500
    DETAILS = "Unknown error happened when handling the request"


class ServiceUnavailable(ClientRequestError):
    CODE = 503
    DETAILS = "Service is temprorarily unavailable because of maintenance"


class UnknownDataError(Exception):
    """
    Some data may be wrong, here is the list
    ----------------------------------------
    - ``location``
    - ``clan label``
    - ``clan league``
    - ``player label``
    - ``player league``
    """

    message: str | None
    data: Any

    MESSAGE: str | None = None

    def __init__(self, data: Any):
        self.data = data
        self.message = self.MESSAGE.format(data=data) if self.MESSAGE else None

        super().__init__(self.message)


class UnknownLocationError(UnknownDataError):
    MESSAGE = "Got an unknown location '{data}!'"


class UnknownClanLabelError(UnknownDataError):
    MESSAGE = "Got an unknown clan label '{data}!'"


class UnknownClanLeagueError(UnknownDataError):
    MESSAGE = "Got an unknown clan league '{data}!'"


class UnknownPlayerLabelError(UnknownDataError):
    MESSAGE = "Got an unknown player label '{data}!'"


class UnknownPlayerLeagueError(UnknownDataError):
    MESSAGE = "Got an unknown player league '{data}'!"
