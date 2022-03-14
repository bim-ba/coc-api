# pyright: strict

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union

import aiohttp
from attrs import field, frozen
from cattrs import structure

from . import utils
from .aliases import (CaseInsensitiveStr, ClanWarFrequency, CountryCode,
                   LabelName, LocationName, PositiveInt, RelativeUrl, Tag)
from .exceptions import UnknownLocationError, UnknownClanLabelError
from .models import Clan, ClanLabel, GoldPass, Location, Player

@frozen
class Client:
    """
    Client class
    """

    token: str

    # _playerLabels: List[PlayerLabel] = field(init=False, default=None)
    # _playerLeagues: List[PlayerLeague] = field(init=False, default=None)
    # _clanLeagues: List[ClanWarLeague] = field(init=False, default=None)
    _clan_labels: List[ClanLabel] = field(init=False, default=None)
    _locations: List[Location] = field(init=False, default=None)

    _uri = 'https://api.clashofclans.com'
    _session: aiohttp.ClientSession = field(init=False, default=None)

    def __attrs_post_init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(created)f] [%(levelname)s] %(message)s'
        )

        object.__setattr__(
            self,
            '_session',
            aiohttp.ClientSession(
                base_url=self._uri,
                headers={
                    'accept': 'application/json',
                    'authorization': f'Bearer {self.token}',
                }
            )
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

                reason = json.get('reason')
                message = json.get('message')

                raise aiohttp.ClientError(
                    f'Invalid request! [{resp.status}] {reason} ("{message}") [{resp.url}]')
            except aiohttp.ContentTypeError as ex:
                logging.error('Error while decoding resp content to JSON. Server returned %d\n[%s]', resp.status, ex)

    async def _fetch(self, path: RelativeUrl, params: Optional[Dict[Any, Any]] = None) -> Dict[Any, Any]:
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

        logging.info('Requesting %s', path)
        async with self._session.get(path, params=params) as resp:
            logging.info('Requested %s [%d]', resp.url, resp.status)
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
        location_data = await self._fetch('/v1/locations')
        for data in location_data['items']:
            obj = structure(data, Location)
            location_list.append(obj)

        object.__setattr__(
            self,
            "_locations",
            location_list
        )

    async def _init_clan_labels_list(self):
        """
        Init ``self._clan_labels`` by fetching data from the server.
        Will fetch only if ``self._clan_labels`` is ``None``.
        """

        if self._clan_labels is not None:
            return

        clan_labels_list: List[ClanLabel] = []
        clan_label_data = await self._fetch('/v1/labels/clans')
        for data in clan_label_data['items']:
            obj = structure(data, ClanLabel)
            clan_labels_list.append(obj)

        object.__setattr__(
            self,
            "_clan_labels",
            clan_labels_list
        )

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
                if location in (loc.countryCode, loc.name)
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
            label_id = next(
                lab.id
                for lab in self._clan_labels
                if label == lab.name
            )
            return label_id
        except StopIteration as stop_iteration:
            raise UnknownClanLabelError(label) from stop_iteration

    async def clans(self, *,
                    name: Optional[str] = None,
                    min_members: Optional[PositiveInt] = None,
                    max_members: Optional[PositiveInt] = None,
                    min_clan_points: Optional[PositiveInt] = None,
                    min_clan_level: Optional[PositiveInt] = None,
                    war_frequency: Optional[ClanWarFrequency] = None,
                    location: Optional[LocationName | CountryCode] = None,
                    labels: Optional[List[LabelName] | LabelName] = None
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
        params = {}
        if name is not None:
            params['name'] = name

        if min_members is not None:
            params['minMembers'] = min_members

        if max_members is not None:
            params['maxMembers'] = max_members

        if min_clan_points is not None:
            params['minClanPoints'] = min_clan_points

        if min_clan_level is not None:
            params['minClanLevel'] = min_clan_level

        if war_frequency is not None:
            params['warFrequency'] = war_frequency

        if location is not None:
            location_id = await self._get_location_id(location)
            params['locationId'] = location_id

        if labels is not None:
            if isinstance(labels, str):
                labels = [labels]

            label_ids = [
                await self._get_clan_label_id(label)
                for label in labels
            ]
            comma_separated_label_ids = ','.join(map(str, label_ids))
            params['labelIds'] = comma_separated_label_ids

        data = await self._fetch('/v1/clans', params=params)
        return [
            clan['tag']
            for clan in data['items']
        ]

    async def clan(self, tag: Tag) -> Clan:
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

        shaped_tag = utils.shape_tag(tag)
        clan_data = await self._fetch(f'/v1/clans/{shaped_tag}')

        member_tags = [member['tag'] for member in clan_data['memberList']]
        clan_data['memberList'] = member_tags

        clan_data['war'] = {
            key[3:].lower(): value
            for key, value in clan_data.items()
            if key.startswith('war')
        }
        clan_data['war']['isWarLogPublic'] = clan_data.pop('isWarLogPublic')

        if clan_data['war']['isWarLogPublic']:
            returned_war_data = await asyncio.gather(
                self._fetch(f'/v1/clans/{shaped_tag}/currentwar'),
                self._fetch(f'/v1/clans/{shaped_tag}/warlog')
            )
            war_data, war_log_data = returned_war_data
            war_state = war_data['state']
            clan_data['war']['state'] = war_state
            clan_data['war']['log'] = war_log_data['items']

            if war_state != 'notInWar':
                clan_data['war']['currentwar'] = war_data

        return structure(clan_data, Clan)

    async def player(self, tag: Tag) -> Player:
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

        shaped_tag = utils.shape_tag(tag)
        player_data = await self._fetch(f'/v1/players/{shaped_tag}')
        player_data['clan'] = player_data['clan']['tag']

        return structure(player_data, Player)

    async def clan_rankings(self, location: Union[LocationName, CountryCode]) -> List[Tag]:
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

        location_id = self._get_location_id(location)
        rankings_data = await self._fetch(f'/v1/locations/{location_id}/rankings/clans')

        tag_list = [clan['tag'] for clan in rankings_data['items']]
        return tag_list

    async def player_rankings(self, location: Union[LocationName, CountryCode]) -> List[Tag]:
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

        location_id = self._get_location_id(location)
        rankings_data = await self._fetch(f'/v1/locations/{location_id}/rankings/players')

        tag_list = [clan['tag'] for clan in rankings_data['items']]
        return tag_list

    async def clan_versus_rankings(self, location: Union[LocationName, CountryCode]) -> List[Tag]:
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

        location_id = self._get_location_id(location)
        rankings_data = await self._fetch(f'/v1/locations/{location_id}/rankings/clans-versus')

        tag_list = [clan['tag'] for clan in rankings_data['items']]
        return tag_list

    async def player_versus_rankings(self, location: Union[LocationName, CountryCode]) -> List[Tag]:
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

        location_id = self._get_location_id(location)
        rankings_data = await self._fetch(f'/v1/locations/{location_id}/rankings/players-versus')

        tag_list = [clan['tag'] for clan in rankings_data['items']]
        return tag_list

    async def goldpass(self) -> GoldPass:
        """
        Get information about the current gold pass season

        Returns
        -------
        GoldPass
            Gold pass object.
        """

        goldpass_data = await self._fetch('/v1/goldpass/seasons/current')
        return structure(goldpass_data, GoldPass)
