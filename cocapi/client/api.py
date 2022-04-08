from typing import Any, Protocol
from dataclasses import dataclass, field

import aiohttp

from ..types import aliases
from ..utils import exceptions


@dataclass
class BaseMethod:
    method: aliases.RequestMethod
    relative_url: aliases.RelativeUrl
    url: aliases.Url = field(init=False)
    base_url: aliases.Url | None = field(init=False, default=None)

    def __post_init__(self):
        if not self.base_url:
            raise AttributeError(
                f"You must define static field ``base_url`` for {self.__class__}"
            )

        self.url = f"{self.base_url}{self.relative_url}"


class CallableWithPlayertag(Protocol):
    # pylint: disable=no-method-argument
    def __call__(*, playertag: str) -> BaseMethod:
        ...


class CallableWithClantag(Protocol):
    # pylint: disable=no-method-argument
    def __call__(*, clantag: str) -> BaseMethod:
        ...


class CallableWithWartag(Protocol):
    # pylint: disable=no-method-argument
    def __call__(*, wartag: str) -> BaseMethod:
        ...


class CallableWithLeagueId(Protocol):
    # pylint: disable=no-method-argument
    def __call__(*, league_id: int) -> BaseMethod:
        ...


class CallableWithLeagueIdAndSeasonId(Protocol):
    # pylint: disable=no-method-argument
    def __call__(*, league_id: int, season_id: int) -> BaseMethod:
        ...


class CallableWithLocationId(Protocol):
    # pylint: disable=no-method-argument
    def __call__(*, location_id: int) -> BaseMethod:
        ...


class Methods:
    class Method(BaseMethod):
        base_url = "https://api.clashofclans.com/v1"

    # clans
    CLANS = lambda: Methods.Method("GET", "/clans")
    CLAN: CallableWithClantag = lambda *, clantag: Methods.Method(
        "GET", f"/clans/{clantag}"
    )
    CLAN_WARLOG: CallableWithClantag = lambda *, clantag: Methods.Method(
        "GET", f"/clans/{clantag}/warlog"
    )
    CLAN_MEMBERS: CallableWithClantag = lambda *, clantag: Methods.Method(
        "GET", f"/clans/{clantag}/members"
    )
    CLAN_CURRENT_WAR: CallableWithClantag = lambda *, clantag: Methods.Method(
        "GET", f"/clans/{clantag}/currentwar"
    )
    CLAN_CURRENT_WAR_LEAGUEGROUP: CallableWithClantag = (
        lambda *, clantag: Methods.Method(
            "GET", f"/clans/{clantag}/currentwar/leaguegroup"
        )
    )
    CLAN_CURRENT_LEAGUE_WAR: CallableWithWartag = lambda *, wartag: Methods.Method(
        "GET", f"/clanwarleagues/wars/{wartag}"
    )

    # players
    PLAYER: CallableWithPlayertag = lambda *, playertag: Methods.Method(
        "GET", f"/players/{playertag}"
    )
    PLAYER_VERIFY_API_TOKEN: CallableWithPlayertag = (
        lambda *, playertag: Methods.Method("GET", f"/players/{playertag}/verifytoken")
    )

    # leagues
    LEAGUES = lambda: Methods.Method("GET", "/leagues")
    LEAGUE_INFO: CallableWithLeagueId = lambda *, league_id: Methods.Method(
        "GET", f"/leagues/{league_id}"
    )
    LEAGUE_SEASONS: CallableWithLeagueId = lambda *, league_id: Methods.Method(
        "GET", f"/leagues/{league_id}/seasons"
    )
    LEAGUE_SEASONS_RANKINGS: CallableWithLeagueIdAndSeasonId = (
        lambda *, league_id, season_id: Methods.Method(
            "GET", f"/leagues/{league_id}/seasons/{season_id}"
        )
    )
    WARLEAGUES = lambda: Methods.Method("GET", "/warleagues")
    WARLEAGUE_INFORMATION: CallableWithLeagueId = lambda *, league_id: Methods.Method(
        "GET", f"/warleagues/{league_id}"
    )

    # locations
    LOCATIONS = lambda: Methods.Method("GET", "/locations")
    LOCATION: CallableWithLocationId = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}"
    )

    # rankings
    CLAN_RANKINGS: CallableWithLocationId = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}/rankings/clans"
    )
    PLAYER_RANKINGS: CallableWithLocationId = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}/rankings/players"
    )
    CLAN_VERSUS_RANKINGS: CallableWithLocationId = (
        lambda *, location_id: Methods.Method(
            "GET", f"/locations/{location_id}/rankings/clans-versus"
        )
    )
    PLAYER_VERSUS_RANKINGS: CallableWithLocationId = (
        lambda *, location_id: Methods.Method(
            "GET", f"/locations/{location_id}/rankings/players-versus"
        )
    )

    # goldpass
    GOLDPASS = lambda: Methods.Method("GET", "/goldpass/seasons/current")

    # labels
    CLAN_LABELS = lambda: Methods.Method("GET", "/labels/clans")
    PLAYER_LABELS = lambda: Methods.Method("GET", "/labels/players")


# not used, but can be
class ServiceMethods:
    class Method(BaseMethod):
        base_url = "https://developer.clashofclans.com/api"

    # developer-api
    LOGIN = lambda: ServiceMethods.Method("POST", "/login")
    LIST_KEY = lambda: ServiceMethods.Method("POST", "/apikey/list")
    CREATE_KEY = lambda: ServiceMethods.Method("POST", "/apikey/create")
    REVOKE_KEY = lambda: ServiceMethods.Method("POST", "/apikey/revoke")


async def check_result(response: aiohttp.ClientResponse):
    """
    Validate request for success.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        Actual response

    Raises
    ------
    ``IncorrectParameters``, ``AccessDenied``, ``ResourceNotFound``,
    ``TooManyRequests``, ``UnknownError``, ``ServiceUnavailable``

    According to the official Clash of Clans API
    --------------------------------------------
    - ``200`` Succesfull response.
    - ``400`` Client provided incorrect parameters for the request.
    - ``403`` Access denied, either because of missing/incorrect credentials or used API token does not grant access to the requested resource.
    - ``404`` Resource was not found.
    - ``429`` Request was throttled, because amount of requests was above the threshold defined for the used API token.
    - ``500`` Unknown error happened when handling the request.
    - ``503`` Service is temprorarily unavailable because of maintenance.
    """

    # because json decoding must be executed in request context manager
    json = await response.json()

    if not response.ok:
        match response.status:
            case 400:
                raise exceptions.IncorrectParameters(response)
            case 403:
                raise exceptions.AccessDenied(response)
            case 404:
                raise exceptions.ResourceNotFound(response)
            case 429:
                raise exceptions.TooManyRequests(response)
            case 503:
                raise exceptions.ServiceUnavailable(response)
            case _:  # 500 also
                response_data = {
                    "error": json.get("error"),
                    "description": json.get("description"),
                    "reason": json.get("reason"),
                    "message": json.get("message"),
                }

                raise exceptions.UnknownError(response, data=response_data)
    return response


async def make_request(
    session: aiohttp.ClientSession,
    api_method: BaseMethod,
    **kwargs: Any,
) -> aiohttp.ClientResponse:
    """
    Parameters
    ----------
    session : ``aiohttp.ClientSession``
        Client session to be used for requests
    api_method : ``BaseMethod``
        Request API method
    **kwargs:
        This keyword arguments are compatible with :meth:``aiohttp.ClientSession.request``

    Returns
    -------
    aiohttp.ClientResponse
        Response object.
    """

    params = kwargs.pop("params", None)
    if params is not None:
        filtered_params = {
            key: value for key, value in params.items() if value is not None
        }
        kwargs["params"] = filtered_params

    try:
        async with session.request(
            method=api_method.method,
            url=api_method.url,
            **kwargs,
        ) as response:
            return await check_result(response)
    except aiohttp.ClientError as error:
        # TODO: either custom exception for that case or integration with `ClientRequestError`
        raise RuntimeError(error) from error
