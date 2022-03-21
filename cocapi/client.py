import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp
import humps.main as humps
from dacite.core import from_dict
from dacite.config import Config

from . import api
from . import utils
from .aliases import (
    CaseInsensitiveStr,
    ClanWarFrequency,
    CountryCode,
    LabelName,
    LocationName,
    PositiveInt,
    RelativeUrl,
    Tag,
)
from .exceptions import UnknownLocationError, UnknownClanLabelError
from .models import Clan, ClanLabel, GoldPass, Location, Player


class Client:
    """
    Client class
    """

    # _playerLabels: List[PlayerLabel] = field(init=False, default=None)
    # _playerLeagues: List[PlayerLeague] = field(init=False, default=None)
    # _clanLeagues: List[ClanWarLeague] = field(init=False, default=None)
    _clan_labels: List[ClanLabel]
    _locations: List[Location]

    _uri = "https://api.clashofclans.com"
    _session: aiohttp.ClientSession
    _event_loop: asyncio.AbstractEventLoop

    def __init__(self, token: str):
        logging.basicConfig(
            level=logging.INFO, format="[%(created)f] [%(levelname)s] %(message)s"
        )

        self._clan_labels = None
        self._locations = None

        self._event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._event_loop)

        self._event_loop.run_until_complete(self._init_http_session(token))

    # def close(self):
    # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
    # self._event_loop.run_until_complete(self._session.close())
    # self._event_loop.run_until_complete(asyncio.sleep(0))

    async def _init_http_session(self, token: str):
        self._session = aiohttp.ClientSession(
            base_url=self._uri,
            headers={
                "accept": "application/json",
                "authorization": f"Bearer {token}",
            },
            connector=aiohttp.TCPConnector(loop=self._event_loop),
        )

    async def _validate_response(self, resp: aiohttp.ClientResponse):
        """
        Validate response for success.
        Normally, this method only called in :meth:`self._fetch` after the actual request.

        Parameters
        ----------
        resp : aiohttp.ClientResponse
            Actual response

        According to the server API
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
        just can be compared with hardcoded codes,
        but for the sake of completeness, reason and detailed message
        about response taken from the server response

        See also
        --------
        :meth:`self._fetch`

        Examples
        --------
        >>> await self._fetch('/v1/clans', params = { 'warFrequency': 1 })
        Exception has occurred: ClientError
        Invalid request! [400] badRequest ("Invalid value for warFrequency parameter.")
        # [400] - response code
        # [badRequest] - reason by server
        # [("...")] - detailed message by server
        """

        if not resp.ok:
            try:
                json = await resp.json()

                reason = json.get("reason")
                message = json.get("message")

                raise aiohttp.ClientError(
                    f'Invalid request! [{resp.status}] {reason} ("{message}") [{resp.url}]'
                )
            except aiohttp.ContentTypeError as ex:
                logging.error(
                    "Error while decoding resp content to JSON. Server returned %d\n[%s]",
                    resp.status,
                    ex,
                )

    async def _fetch(
        self, path: RelativeUrl, params: Optional[Dict[Any, Any]] = None
    ) -> Dict[Any, Any]:
        """
        Fetch resource with base url https://api.clashofclans.com/

        This function simply concatenate base url and ``path``.
        Then it will make ``GET`` request with specified params (or without).

        Parameters
        ----------
        path : str
            Relative path.
        params : dict, default None
            Params to pass with request.

        Returns
        -------
        dict
            JSON-representable dict.

        Examples
        --------
        >>> await self._fetch('/v1/clans/%232PQC8YLR9') # tag is #2PQC8YLR9
        {'tag': '#2PQC8YLR9', 'name': 'Bomb', 'type': 'closed', ...}
        >>> await self._fetch('/v1/locations')
        {'items': [{...}, {...}, {...}], ...}
        >>> await self._fetch('/v1/clans', params = { 'name': 'bomb' })
        {'items': [{...}, {...}, {...}], ...}
        """
        filtered_params = params
        if params is not None:
            filtered_params = {
                key: value for key, value in params.items() if value is not None
            }

        logging.info("Requesting %s", path)
        async with self._session.get(path, params=filtered_params) as resp:
            logging.info("Requested %s [%d]", resp.url, resp.status)
            await self._validate_response(resp)
            return await resp.json()

    async def _init_location_list(self):
        """
        Init ``self._locations`` by fetching data from the server.
        Will fetch only if ``self._locations`` is ``None``.
        """

        if self._locations is not None:
            return

        location_list: List[Location] = []
        location_raw_data = await self._fetch(api.Methods.LOCATIONS())
        location_cooked_data = humps.decamelize(location_raw_data)

        for data in location_cooked_data["items"]:
            location = from_dict(
                data_class=Location,
                data=data,
                config=Config(type_hooks={str: str.lower}),
            )
            location_list.append(location)

        self._locations = location_list

    async def _init_clan_labels_list(self):
        """
        Init ``self._clan_labels`` by fetching data from the server.
        Will fetch only if ``self._clan_labels`` is ``None``.
        """

        if self._clan_labels is not None:
            return

        clan_labels_list: List[ClanLabel] = []
        clan_label_raw_data = await self._fetch(api.Methods.CLAN_LABELS())
        clan_label_cooked_data = humps.decamelize(clan_label_raw_data)

        for data in clan_label_cooked_data["items"]:
            clan_label = from_dict(
                data_class=ClanLabel,
                data=data,
                config=Config(type_hooks={str: str.lower}),
            )
            clan_labels_list.append(clan_label)

        self._clan_labels = clan_labels_list

    async def _get_location_id(self, location: CaseInsensitiveStr):
        """
        Converts location as string to location id by searching through
        available locations in ``self._locations``.

        Parameters
        ----------
        location : str
            [CaseInsentive]
            Location full name or just country code.

        Returns
        -------
        int
            Location id.

        Throws
        ------
        UnknownLocationError
            If location name or location code is unknown.

        Remarks
        -------
        - May fetch locations from server if not initialized. See :meth:``self._init_locations_list``

        Examples
        --------
        >>> await self._get_location_id('KeNYa')
        32000126
        >>> await self._get_location_id('ru')
        32000193
        """

        if self._locations is None:
            await self._init_location_list()

        location = location.lower()

        try:
            location_id = next(
                loc.id
                for loc in self._locations
                if location in (loc.country_code, loc.name)
            )
            return location_id
        except StopIteration as stop_iteration:
            raise UnknownLocationError(location) from stop_iteration

    async def _get_clan_label_id(self, label: CaseInsensitiveStr):
        """
        Converts clan label as string to clan label id by searching through
        available clan labels in ``self._clan_labels``.

        Parameters
        ----------
        label : str
            [CaseInsentive]
            Label name.

        Returns
        -------
        int
            Clan label id.

        Throws
        ------
        UnknownClanLabelError
            If clan label is unknown.

        Remarks
        -------
        - May fetch clan labels from server if not initialized. See :meth:``self._init_clan_labels_list``

        Examples
        --------
        >>> await self._get_clan_label_id('InternatiONAL')
        56000007
        >>> await self._get_clan_label_id('CLAN GAMES')
        56000004
        """

        if self._clan_labels is None:
            await self._init_clan_labels_list()

        label = label.lower()

        try:
            label_id = next(lab.id for lab in self._clan_labels if label == lab.name)
            return label_id
        except StopIteration as stop_iteration:
            raise UnknownClanLabelError(label) from stop_iteration

    async def _clans(self, **kwargs: Any) -> List[Tag]:
        params = humps.camelize(kwargs)
        if params.get("location"):
            del params["location"]
        if params.get("labels"):
            del params["labels"]

        if kwargs.get("location"):
            raw_location = kwargs["location"]
            location_id = await self._get_location_id(raw_location)
            params["locationId"] = location_id

        if kwargs.get("labels"):
            raw_labels = kwargs["labels"]
            if isinstance(raw_labels, str):
                raw_labels = [raw_labels]

            label_ids = [
                await self._get_clan_label_id(raw_label) for raw_label in raw_labels
            ]
            comma_separated_label_ids = ",".join(map(str, label_ids))
            params["labelIds"] = comma_separated_label_ids

        data = await self._fetch(api.Methods.CLANS(), params=params)
        return [clan["tag"] for clan in data["items"]]

    def clans(
        self,
        *,
        name: Optional[str] = None,
        min_members: Optional[PositiveInt] = None,
        max_members: Optional[PositiveInt] = None,
        min_clan_points: Optional[PositiveInt] = None,
        min_clan_level: Optional[PositiveInt] = None,
        war_frequency: Optional[ClanWarFrequency] = None,
        location: Optional[LocationName | CountryCode] = None,
        labels: Optional[List[LabelName] | LabelName] = None,
    ) -> List[Tag]:
        """
        Search all clans by name and/or filtering the results using various criteria.
        At least one filtering criteria must be defined and if name is used as part of search,
        it is required to be at least three characters long.
        It is not possible to specify ordering for results
        so clients should not rely on any specific ordering as that may change
        in the future releases of the API.

        Parameters
        ----------
        name : str
            Clan name
        min_members : int [PositiveInt]
            Min clan members
        max_members : int [PositiveInt]
            Max clan members
        min_clan_points : int [PositiveInt]
            Min clan points
        min_clan_level : int [PositiveInt]
            Min clan level
        war_frequency : str [ClanWarFrequency]
            War frequency as literal, see `ClanWarFrequency`
        location : str
            [CaseInsentiveStr]
            Location name or country code
        labels : list[str] | str
            [CaseInsentive]
            List of clan labels or just 1 clan label

        Returns
        -------
        List of clan tags.

        Examples
        --------
        >>> a = await coc.clans(location='ru', war_frequency='never')
        ['#RLU20URV', '#RV9RCQV', '#2LVV8RCJJ', ...]
        """
        return self._event_loop.run_until_complete(
            self._clans(
                name=name,
                min_members=min_members,
                max_members=max_members,
                min_clan_points=min_clan_points,
                min_clan_level=min_clan_level,
                war_frequency=war_frequency,
                location=location,
                labels=labels,
            )
        )

    async def _clan(self, tag: Tag) -> Clan:
        shaped_tag = utils.shape_tag(tag)
        clan_data = await self._fetch(api.Methods.CLAN(clantag=shaped_tag))

        member_tags = [member["tag"] for member in clan_data["memberList"]]
        clan_data["memberList"] = member_tags

        clan_data["war"] = {}
        clan_data["war"]["wins"] = clan_data.pop("warWins")
        clan_data["war"]["losses"] = clan_data.pop("warLosses")
        clan_data["war"]["ties"] = clan_data.pop("warTies")
        clan_data["war"]["winstreak"] = clan_data.pop("warWinStreak")
        clan_data["war"]["frequency"] = clan_data.pop("warFrequency")
        clan_data["war"]["isWarLogPublic"] = clan_data.pop("isWarLogPublic")
        clan_data["war"]["league"] = clan_data.pop("warLeague")

        if clan_data["war"]["isWarLogPublic"]:
            returned_war_data = await asyncio.gather(
                self._fetch(api.Methods.CLAN_CURRENT_WAR(clantag=shaped_tag)),
                self._fetch(api.Methods.CLAN_WARLOG(clantag=shaped_tag)),
            )
            war_data, war_log_data = returned_war_data
            war_state = war_data["state"]

            clan_data["war"]["state"] = war_state
            clan_data["war"]["log"] = war_log_data["items"]

            if war_state != "notInWar":
                clan_data["war"]["currentwar"] = war_data

        cooked_clan_data = humps.decamelize(clan_data)
        return from_dict(
            data_class=Clan,
            data=cooked_clan_data,
            config=Config(type_hooks={str: utils.rawtime_to_datetime}),
        )

    def clan(self, tag: Tag) -> Clan:
        """
        Get information about a single clan by clan tag.
        Clan tags can be found using clan search operation.
        Note that clan tags start with hash character '#'.

        Parameters
        ----------
        tag : str
            Tag.

        Returns
        -------
        Clan
            Clan object.

        Remarks
        -------
        Performs 1 or 3 requests:
        - '/clans/{tag}' (always)

        If clan war log is public:
            - '/clans/{tag}/currentwar' (information about current war)
            - '/clans/{tag}/warlog' (log all war results)
        """
        return self._event_loop.run_until_complete(self._clan(tag))

    async def _player(self, tag: Tag) -> Player:
        shaped_tag = utils.shape_tag(tag)
        player_data = await self._fetch(api.Methods.PLAYER(playertag=shaped_tag))
        player_data["clan"] = player_data["clan"]["tag"]
        cooked_player_data = humps.decamelize(player_data)

        return from_dict(data_class=Player, data=cooked_player_data)

    def player(self, tag: Tag) -> Player:
        """
        Get information about a single player by player tag.
        Player tags can be found either in game or by from clan member lists.
        Note that player tags start with hash character '#'.

        Parameters
        ----------
        tag : str
            Tag.

        Returns
        -------
        Player
            Player object.
        """
        return self._event_loop.run_until_complete(self._player(tag))

    async def _clan_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
        location_id = await self._get_location_id(location)
        rankings_data = await self._fetch(
            api.Methods.CLAN_RANKINGS(location_id=location_id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    def clan_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
        """
        Get clan rankings for a specific location

        Parameters
        ----------
        location : str
            Location name or its code

        Returns
        -------
        list[str]
            List of clan tags (descending by score)
        """
        return self._event_loop.run_until_complete(self._clan_rankings(location))

    async def _player_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
        location_id = await self._get_location_id(location)
        rankings_data = await self._fetch(
            api.Methods.PLAYER_RANKINGS(location_id=location_id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    def player_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
        """
        Get player rankings for a specific location

        Parameters
        ----------
        location : str
            Location name or its code

        Returns
        -------
        list[str]
            List of player tags (descending by trophies)
        """
        return self._event_loop.run_until_complete(self._player_rankings(location))

    async def _clan_versus_rankings(
        self, location: LocationName | CountryCode
    ) -> List[Tag]:
        """
        Get clan versus rankings for a specific location

        Parameters
        ----------
        location : str
            Location name or its code

        Returns
        -------
        list[str]
            List of clan tags (descending by versus score)
        """

        location_id = await self._get_location_id(location)
        rankings_data = await self._fetch(
            api.Methods.CLAN_VERSUS_RANKINGS(location_id=location_id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    def clan_versus_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
        """
        Get clan versus rankings for a specific location

        Parameters
        ----------
        location : str
            Location name or its code

        Returns
        -------
        list[str]
            List of clan tags (descending by versus score)
        """
        return self._event_loop.run_until_complete(self._clan_versus_rankings(location))

    async def _player_versus_rankings(
        self, location: LocationName | CountryCode
    ) -> List[Tag]:
        location_id = await self._get_location_id(location)
        rankings_data = await self._fetch(
            api.Methods.PLAYER_VERSUS_RANKINGS(location_id=location_id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    def player_versus_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
        """
        Get player versus rankings for a specific location

        Parameters
        ----------
        location : str
            Location name or its code

        Returns
        -------
        list[str]
            List of player tags (descending by versus trophies)
        """
        return self._event_loop.run_until_complete(
            self._player_versus_rankings(location)
        )

    async def _goldpass(self) -> GoldPass:
        goldpass_raw_data = await self._fetch(api.Methods.GOLDPASS())
        goldpass_cooked_data = humps.decamelize(goldpass_raw_data)
        return from_dict(
            data_class=GoldPass,
            data=goldpass_cooked_data,
            config=Config(type_hooks={str: utils.rawtime_to_datetime}),
        )

    def goldpass(self) -> GoldPass:
        """
        Get information about the current gold pass season

        Returns
        -------
        GoldPass
            Gold pass object.
        """
        return self._event_loop.run_until_complete(self._goldpass())
