from dataclasses import dataclass
from typing import Optional, Dict, Any

import aiohttp
import humps.main as humps

from cocapi.exceptions import ClientRequestError, JSONContentTypeError

from .aliases import RelativeUrl, RequestMethod


@dataclass(frozen=True)
class Method:
    method: RequestMethod
    url: RelativeUrl


class Methods:
    # clans
    CLANS = lambda: Method("GET", "/v1/clans")
    CLAN = lambda *, clantag: Method("GET", f"/v1/clans/{clantag}")
    CLAN_WARLOG = lambda *, clantag: Method("GET", f"/v1/clans/{clantag}/warlog")
    CLAN_MEMBERS = lambda *, clantag: Method("GET", f"/v1/clans/{clantag}/members")
    CLAN_CURRENT_WAR = lambda *, clantag: Method(
        "GET", f"/v1/clans/{clantag}/currentwar"
    )
    CLAN_CURRENT_WAR_LEAGUEGROUP = lambda *, clantag: Method(
        "GET", f"/v1/clans/{clantag}/currentwar/leaguegroup"
    )
    CLAN_CURRENT_LEAGUE_WAR = lambda *, wartag: Method(
        "GET", f"/v1/clanwarleagues/wars/{wartag}"
    )

    # players
    PLAYER = lambda *, playertag: Method("GET", f"/v1/players/{playertag}")
    PLAYER_VERIFY_API_TOKEN = lambda *, playertag: Method(
        "GET", f"/v1/players/{playertag}/verifytoken"
    )

    # leagues
    LEAGUES = lambda: Method("GET", "/v1/leagues")
    LEAGUE_INFO = lambda *, league_id: Method("GET", f"/v1/leagues/{league_id}")
    LEAGUE_SEASONS = lambda *, league_id: Method(
        "GET", f"/v1/leagues/{league_id}/seasons"
    )
    LEAGUE_SEASONS_RANKINGS = lambda *, league_id, season_id: Method(
        "GET", f"/v1/leagues/{league_id}/seasons/{season_id}"
    )
    WARLEAGUES = lambda: Method("GET", "/v1/warleagues")
    WARLEAGUE_INFORMATION = lambda *, league_id: Method(
        "GET", f"/v1/warleagues/{league_id}"
    )

    # locations
    LOCATIONS = lambda: Method("GET", "/v1/locations")
    LOCATION = lambda *, location_id: Method("GET", f"/v1/locations/{location_id}")

    # rankings
    CLAN_RANKINGS = lambda *, location_id: Method(
        "GET", f"/v1/locations/{location_id}/rankings/clans"
    )
    PLAYER_RANKINGS = lambda *, location_id: Method(
        "GET", f"/v1/locations/{location_id}/rankings/players"
    )
    CLAN_VERSUS_RANKINGS = lambda *, location_id: Method(
        "GET", f"/v1/locations/{location_id}/rankings/clans-versus"
    )
    PLAYER_VERSUS_RANKINGS = lambda *, location_id: Method(
        "GET", f"/v1/locations/{location_id}/rankings/players-versus"
    )

    # goldpass
    GOLDPASS = lambda: Method("GET", "/v1/goldpass/seasons/current")

    # labels
    CLAN_LABELS = lambda: Method("GET", "/v1/labels/clans")
    PLAYER_LABELS = lambda: Method("GET", "/v1/labels/players")


async def check_result(resp: aiohttp.ClientResponse) -> Dict[Any, Any]:
    """
    Validate response for success.
    Normally, this method only called in :meth:``self._fetch`` after the actual request.

    Parameters
    ----------
    resp : aiohttp.ClientResponse
        Actual response

    According to the official Clash of Clans API
    ----------------------------
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
    >>> await self.make_request('/v1/clans', params = { 'warFrequency': 1 })
    Exception has occurred: ClientError
    Invalid request! [400] badRequest ("Invalid value for warFrequency parameter.")
    # [400] - response code
    # [badRequest] - reason by server
    # [("...")] - detailed message by server
    """

    try:
        json = await resp.json()

        if not resp.ok:

            reason = json.get("reason")
            message = json.get("message")

            raise ClientRequestError(resp, custom_reason=reason, custom_message=message)
    except aiohttp.ContentTypeError as error:
        raise JSONContentTypeError(resp.content_type, error) from error

    decamelized = humps.decamelize(json)
    return decamelized


async def make_request(
    session: aiohttp.ClientSession,
    method: Method,
    *,
    params: Optional[Dict[Any, Any]] = None,
) -> Dict[Any, Any]:
    """
    Parameters
    ----------
    session : ``aiohttp.ClientSession``
        Client session to be used for requests
    method : ``Method``
        Request method
    params : dict = None
        Params to pass with request.

    Returns
    -------
    dict
        JSON-representable dict.

    Examples
    --------
    >>> await make_request('/v1/clans/%232PQC8YLR9') # tag is #2PQC8YLR9
    {'tag': '#2PQC8YLR9', 'name': 'Bomb', 'type': 'closed', ...}
    >>> await make_request('/v1/locations')
    {'items': [{...}, {...}, {...}], ...}
    >>> await make_request('/v1/clans', params = { 'name': 'bomb' })
    {'items': [{...}, {...}, {...}], ...}
    """

    filtered_params = params
    if params is not None:
        filtered_params = {
            key: value for key, value in params.items() if value is not None
        }

    try:
        async with session.request(
            method=method.method, url=method.url, params=filtered_params
        ) as resp:
            return await check_result(resp)
    except aiohttp.ClientError as error:
        # TODO: either custom exception for that case or integration with `ClientRequestError`
        raise RuntimeError(error) from error
