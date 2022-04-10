from typing import Any, Optional
from dataclasses import dataclass, field

import aiohttp

from ..types import aliases
from ..types import exceptions


@dataclass
class BaseMethod:
    # config
    base_url: aliases.Url | None = field(init=False, default=None)
    default_http_method: aliases.RequestMethod | None = field(init=False, default=None)

    # actual dataclass members
    path: aliases.RelativeUrl
    method: Optional[aliases.RequestMethod] = None
    url: aliases.Url = field(init=False)

    def __post_init__(self):
        if not self.base_url:
            raise NotImplementedError(
                f"You must define static field 'base_url' for {self.__class__}"
            ) from None

        if not self.method and not self.default_http_method:
            raise NotImplementedError(
                f"You must define either static field 'default_http_method' or pass it directly in {self.__class__}"
            ) from None

        self.method = self.default_http_method if self.method is None else self.method
        self.url = self.base_url + self.path

    def __call__(self, **kwargs: Any):
        try:
            self.url = self.url.format(**kwargs)
            return self
        except KeyError as error:
            (missing_field,) = error.args
            raise KeyError(
                f"Missing field: '{missing_field}' when formatting {self.url}"
            ) from error


class Methods:
    class Method(BaseMethod):
        base_url = "https://api.clashofclans.com/v1"
        default_http_method = "GET"

    # clans
    CLANS = Method("/clans")
    """`GET`: `/clans`"""
    CLAN = Method("/clans/{clantag}")
    """`GET`: `/clans/{clantag:str}`"""
    CLAN_WARLOG = Method("/clans/{clantag}/warlog")
    """`GET`: `/clans/{clantag:str}/warlog`"""
    CLAN_MEMBERS = Method("/clans/{clantag}/members")
    """`GET`: `/clans/{clantag:str}/members`"""
    CLAN_CURRENT_WAR = Method("/clans/{clantag}/currentwar")
    """`GET`: `/clans/{clantag:str}/currentwar`"""
    CLAN_CURRENT_WAR_LEAGUEGROUP = Method("/clans/{clantag}/currentwar/leaguegroup")
    """`GET`: `/clans/{clantag:str}/currentwar/leaguegroup`"""
    CLAN_CURRENT_LEAGUE_WAR = Method("/clanwarleagues/wars/{wartag}")
    """`GET`: `/clanwarleagues/wars/{wartag:str}`"""

    # players
    PLAYER = Method("/players/{playertag}")
    """`GET`: `/players/{playertag:str}`"""
    PLAYER_VERIFY_API_TOKEN = Method("/players/{playertag}/verifytoken", "POST")
    """`POST`: `/players/{playertag:str}/verifytoken`"""

    # leagues
    LEAGUES = Method("/leagues")
    """`GET`: `/leagues`"""
    LEAGUE_INFO = Method("/leagues/{league_id}")
    """`GET`: `/leagues/{league_id:int}`"""
    LEAGUE_SEASONS = Method("/leagues/{league_id}/seasons")
    """`GET`: `/leagues/{league_id:int}/seasons`"""
    LEAGUE_SEASONS_RANKINGS = Method("/leagues/{league_id}/seasons/{season_id}")
    """`GET`: `/leagues/{league_id:int}/seasons/{season_id:int}`"""
    WARLEAGUES = Method("/warleagues")
    """`GET`: `/warleagues`"""
    WARLEAGUE_INFORMATION = Method("/warleagues/{league_id}")
    """`GET`: `/warleagues/{league_id:int}`"""

    # locations
    LOCATIONS = Method("/locations")
    """`GET`: `/locations`"""
    LOCATION = Method("/locations/{location_id}")
    """`GET`: `/locations/{location_id:int}`"""

    # rankings
    CLAN_RANKINGS = Method("/locations/{location_id}/rankings/clans")
    """`GET`: `/locations/{location_id:int}/rankings/clans`"""
    PLAYER_RANKINGS = Method("/locations/{location_id}/rankings/players")
    """`GET`: `/locations/{location_id:int}/rankings/players`"""
    CLAN_VERSUS_RANKINGS = Method("/locations/{location_id}/rankings/clans-versus")
    """`GET`: `/locations/{location_id:int}/rankings/clans-versus`"""
    PLAYER_VERSUS_RANKINGS = Method("/locations/{location_id}/rankings/players-versus")
    """`GET`: `/locations/{location_id:int}/rankings/players-versus`"""

    # goldpass
    GOLDPASS = Method("/goldpass/seasons/current")
    """`GET`: `/goldpass/seasons/current`"""

    # labels
    CLAN_LABELS = Method("/labels/clans")
    """`GET`: `/labels/clans`"""
    PLAYER_LABELS = Method("/labels/players")
    """`GET`: `/labels/players`"""


# not used, but can be
class ServiceMethods:
    class Method(BaseMethod):
        base_url = "https://developer.clashofclans.com/api"
        default_http_method = "POST"

    # developer-api
    LOGIN = Method("/login")
    """`POST`: `/login`"""
    LIST_KEY = Method("/apikey/list")
    """`POST`: `/apikey/list`"""
    CREATE_KEY = Method("/apikey/create")
    """`POST`: `/apikey/create`"""
    REVOKE_KEY = Method("/apikey/revoke")
    """`POST`: `/apikey/revoke`"""


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

    async with session.request(
        method=api_method.method,  # type: ignore
        url=api_method.url,
        **kwargs,
    ) as response:
        return await check_result(response)
