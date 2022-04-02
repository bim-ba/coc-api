from dataclasses import dataclass, field
from typing import Any

import aiohttp
import humps.main as humps


from .aliases import RelativeUrl, Url, RequestMethod
from .exceptions import ClientRequestError, JSONContentTypeError


@dataclass
class BaseMethod:
    method: RequestMethod
    relative_url: RelativeUrl
    url: Url = field(init=False)
    base_url: Url | None = field(init=False, default=None)

    def __post_init__(self):
        if not self.base_url:
            raise AttributeError(
                f"You must define static field ``base_url`` for {self.__class__}"
            )

        self.url = f"{self.base_url}{self.relative_url}"


class Methods:
    @dataclass
    class Method(BaseMethod):
        base_url = "https://api.clashofclans.com/v1"

    # clans
    CLANS = lambda: Methods.Method("GET", "/clans")
    CLAN = lambda *, clantag: Methods.Method("GET", f"/clans/{clantag}")
    CLAN_WARLOG = lambda *, clantag: Methods.Method("GET", f"/clans/{clantag}/warlog")
    CLAN_MEMBERS = lambda *, clantag: Methods.Method("GET", f"/clans/{clantag}/members")
    CLAN_CURRENT_WAR = lambda *, clantag: Methods.Method(
        "GET", f"/clans/{clantag}/currentwar"
    )
    CLAN_CURRENT_WAR_LEAGUEGROUP = lambda *, clantag: Methods.Method(
        "GET", f"/clans/{clantag}/currentwar/leaguegroup"
    )
    CLAN_CURRENT_LEAGUE_WAR = lambda *, wartag: Methods.Method(
        "GET", f"/clanwarleagues/wars/{wartag}"
    )

    # players
    PLAYER = lambda *, playertag: Methods.Method("GET", f"/players/{playertag}")
    PLAYER_VERIFY_API_TOKEN = lambda *, playertag: Methods.Method(
        "GET", f"/players/{playertag}/verifytoken"
    )

    # leagues
    LEAGUES = lambda: Methods.Method("GET", "/leagues")
    LEAGUE_INFO = lambda *, league_id: Methods.Method("GET", f"/leagues/{league_id}")
    LEAGUE_SEASONS = lambda *, league_id: Methods.Method(
        "GET", f"/leagues/{league_id}/seasons"
    )
    LEAGUE_SEASONS_RANKINGS = lambda *, league_id, season_id: Methods.Method(
        "GET", f"/leagues/{league_id}/seasons/{season_id}"
    )
    WARLEAGUES = lambda: Methods.Method("GET", "/warleagues")
    WARLEAGUE_INFORMATION = lambda *, league_id: Methods.Method(
        "GET", f"/warleagues/{league_id}"
    )

    # locations
    LOCATIONS = lambda: Methods.Method("GET", "/locations")
    LOCATION = lambda *, location_id: Methods.Method("GET", f"/locations/{location_id}")

    # rankings
    CLAN_RANKINGS = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}/rankings/clans"
    )
    PLAYER_RANKINGS = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}/rankings/players"
    )
    CLAN_VERSUS_RANKINGS = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}/rankings/clans-versus"
    )
    PLAYER_VERSUS_RANKINGS = lambda *, location_id: Methods.Method(
        "GET", f"/locations/{location_id}/rankings/players-versus"
    )

    # goldpass
    GOLDPASS = lambda: Methods.Method("GET", "/goldpass/seasons/current")

    # labels
    CLAN_LABELS = lambda: Methods.Method("GET", "/labels/clans")
    PLAYER_LABELS = lambda: Methods.Method("GET", "/labels/players")


class ServiceMethods:
    @dataclass
    class Method(BaseMethod):
        base_url = "https://developer.clashofclans.com/api"

    # developer-api
    LOGIN = lambda: ServiceMethods.Method("POST", "/login")
    LIST_KEY = lambda: ServiceMethods.Method("POST", "/apikey/list")
    CREATE_KEY = lambda: ServiceMethods.Method("POST", "/apikey/create")
    REVOKE_KEY = lambda: ServiceMethods.Method("POST", "/apikey/revoke")


async def jsonify(response: aiohttp.ClientResponse, *, decamelize: bool = True):
    """
    Decodes ``response.content`` into JSON and returns it.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        Actual response
    decamelize : bool (default = `True`)
        If `True`, JSON keys will be automatically decamelized

    Returns
    -------
    JSON-formatted content

    Remarks
    -------
    Actually, real decoding is performed in :meth:``api.check_result`` due to the ``aiohttp`` design.
    In detail, this method just grabs ``response.content._body`` and returns it.

    Examples
    --------
    >>> resp = await api.make_request(api.Methods.CLANS(), params={
        'name': 'bomb',
        'warFrequency': 'always'
    })
    >>> json = await api.jsonify(resp)
    # TODO: ...
    """

    try:
        json = await response.json()

        if decamelize:
            decamelized = humps.decamelize(json)
            return decamelized
        return json
    except aiohttp.ContentTypeError as error:
        raise JSONContentTypeError(response.content_type, error) from error


async def check_result(response: aiohttp.ClientResponse):
    """
    Validate response for success.
    Normally, this method only called in :meth:``make_request``.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        Actual response

    According to the official Clash of Clans API
    --------------------------------------------
    - ``200`` Succesfull response.
    - ``400`` Client provided incorrect parameters for the request.
    - ``403`` Access denied, either because of missing/incorrect credentials or used API token does not grant access to the requested resource.
    - ``404`` Resource was not found.
    - ``429`` Request was throttled, because amount of requests was above the threshold defined for the used API token.
    - ``500`` Unknown error happened when handling the request.
    - ``503`` Service is temprorarily unavailable because of maintenance.

    Remarks
    -------
    Response codes, however, can be hardcoded and response code
    just can be compared with hardcoded ones,
    but for the sake of completeness, reason and detailed message
    about response taken from the server response

    See also
    --------
    :meth:``make_request``

    Examples
    --------
    >>> await api.make_request(api.Methods.CLANS(), params={
        'warFrequency': 1
    })
    TODO: ...
    """

    # because json decoding must be executed in request context manager
    json = await jsonify(response, decamelize=False)

    if not response.ok:
        data = {
            "error": json.get("error"),
            "description": json.get("description"),
            "reason": json.get("reason"),
            "message": json.get("message"),
        }

        raise ClientRequestError(response, data=data)
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

    Examples
    --------
    >>> await api.make_request(api.Methods.CLAN(clantag='#2PQC8YLR9'))
    #TODO: ...
    >>> await api.make_request(api.Methods.LOCATIONS())
    #TODO: ...
    >>> await api.make_request(api.Methods.CLANS(), params = { 'name': 'bomb' })
    #TODO: ...
    """

    params = kwargs.pop("params", None)
    filtered_params = None
    if params is not None:
        filtered_params = {
            key: value for key, value in params.items() if value is not None
        }

    try:
        async with session.request(
            method=api_method.method,
            url=api_method.url,
            params=filtered_params,
            **kwargs,
        ) as response:
            return await check_result(response)
    except aiohttp.ClientError as error:
        # TODO: either custom exception for that case or integration with `ClientRequestError`
        raise RuntimeError(error) from error
