import asyncio
import logging
from typing import Dict, List, Optional, Text

import aiohttp
import dacite.core as dacite
import dacite.config


from . import api
from . import utils
from .aliases import (
    ClanWarFrequency,
    CountryCode,
    LabelName,
    LocationName,
    PositiveInt,
    Tag,
)
from .exceptions import UnknownLocationError, UnknownClanLabelError
from .models import (
    Clan,
    ClanLabel,
    ClanWarLeague,
    GoldPass,
    Location,
    Player,
    PlayerLabel,
    PlayerLeague,
)
from .baseclient import BaseClient


class Client(BaseClient):
    """
    Client class
    """

    _uri = "https://api.clashofclans.com"

    _locations: Dict[Text, Location]
    _clan_labels: Dict[Text, ClanLabel]
    _clan_leagues: Dict[Text, ClanWarLeague]
    _player_labels: Dict[Text, PlayerLabel]
    _player_leagues: Dict[Text, PlayerLeague]

    __token: Text
    __session: aiohttp.ClientSession

    # public properties
    @property
    def uri(self):
        return self._uri

    # private properties
    @property
    def _token(self):
        return self.__token

    @property
    def _session(self):
        return self.__session

    def __init__(self, token: Text):
        logging.basicConfig(
            level=logging.WARNING, format="[%(created)f] [%(levelname)s] %(message)s"
        )

        try:
            _ = asyncio.get_running_loop()
        except RuntimeError as error:
            raise RuntimeError(
                "Client class should be instantiated only within async method!"
            ) from error

        self.__token = token
        self.__session = aiohttp.ClientSession(
            base_url=self._uri,
            headers={
                "accept": "application/json",
                "authorization": f"Bearer {token}",
            },
            timeout=aiohttp.ClientTimeout(total=60),
        )

    async def close(self):
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await self.__session.close()
        await asyncio.sleep(0)

    async def _init_locations(self):
        """
        Init ``self._locations`` by fetching data from the server.
        """

        location_mapping = {}
        location_data = await api.make_request(self.__session, api.Methods.LOCATIONS())

        for data in location_data["items"]:
            location = dacite.from_dict(
                data_class=Location,
                data=data,
                config=dacite.config.Config(type_hooks={str: str.lower}),
            )

            if location.name:
                location_mapping[location.name] = location
            if location.country_code:
                location_mapping[location.country_code] = location

        self._locations = location_mapping

    async def _init_clan_labels(self):
        """
        Init ``self._clan_labels`` by fetching data from the server.
        """

        clan_labels_mapping = {}
        clan_label_data = await api.make_request(
            self.__session, api.Methods.CLAN_LABELS()
        )

        for data in clan_label_data["items"]:
            clan_label = dacite.from_dict(
                data_class=ClanLabel,
                data=data,
                config=dacite.config.Config(type_hooks={str: str.lower}),
            )

            clan_labels_mapping[clan_label.name] = clan_label

        self._clan_labels = clan_labels_mapping

    async def _init_clan_leagues(self):
        """
        Init ``self._clan_leagues`` by fetching data from the server.
        """

        clan_leagues_mapping = {}
        clan_leagues_data = await api.make_request(
            self.__session, api.Methods.WARLEAGUES()
        )

        for data in clan_leagues_data["items"]:
            clan_league = dacite.from_dict(
                data_class=ClanWarLeague,
                data=data,
                config=dacite.config.Config(type_hooks={str: str.lower}),
            )

            clan_leagues_mapping[clan_league.name] = clan_league

        self._clan_leagues = clan_leagues_mapping

    async def _init_player_labels(self):
        """
        Init ``self._player_labels`` by fetching data from the server.
        """

        player_labels_mapping = {}
        player_labels_data = await api.make_request(
            self.__session, api.Methods.WARLEAGUES()
        )

        for data in player_labels_data["items"]:
            player_label = dacite.from_dict(
                data_class=PlayerLabel,
                data=data,
                config=dacite.config.Config(type_hooks={str: str.lower}),
            )

            player_labels_mapping[player_label.name] = player_label

        self._player_labels = player_labels_mapping

    async def _init_player_leagues(self):
        """
        Init ``self._player_leagues`` by fetching data from the server.
        """

        player_leagues_mapping = {}
        player_leagues_data = await api.make_request(
            self.__session, api.Methods.WARLEAGUES()
        )

        for data in player_leagues_data["items"]:
            player_league = dacite.from_dict(
                data_class=PlayerLeague,
                data=data,
                config=dacite.config.Config(type_hooks={str: str.lower}),
            )

            player_leagues_mapping[player_league.name] = player_league

        self._player_leagues = player_leagues_mapping

    async def clans(
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
        min_members : int
            Min clan members
        max_members : int
            Max clan members
        min_clan_points : int
            Min clan points
        min_clan_level : int
            Min clan level
        war_frequency : str
            War frequency as literal, see ``ClanWarFrequency``
        location : str
            Location name or country code
        labels : list[str] | str
            List of clan labels or just 1 clan label

        Returns
        -------
        List of clan tags.

        Examples
        --------
        >>> await client.clans(location='ru', war_frequency='never')
        ['#RLU20URV', '#RV9RCQV', '#2LVV8RCJJ', ...]
        """

        params = {}

        if name:
            params["name"] = name

        if min_members:
            params["minMembers"] = min_members

        if max_members:
            params["maxMembers"] = max_members

        if min_clan_points:
            params["minClanPoints"] = min_clan_points

        if min_clan_level:
            params["minClanLevel"] = min_clan_level

        if war_frequency:
            params["warFrequency"] = war_frequency

        if location:
            loc = await self.get_location(location)
            loc_id = loc.id
            params["locationId"] = loc_id

        if labels:
            if isinstance(labels, str):
                labels = [labels]

            lab_ids = []

            for lab in labels:
                lab = lab.lower()
                clan_lab = await self.get_clan_label(lab)
                lab_ids.append(clan_lab.id)

            # [1, 2, 3] => "1,2,3"
            comma_separated_lab_ids = ",".join(map(str, lab_ids))
            params["labelIds"] = comma_separated_lab_ids

        clans_data = await api.make_request(
            self.__session, api.Methods.CLANS(), params=params
        )
        tag_list = [clan["tag"] for clan in clans_data["items"]]
        return tag_list

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

        Examples
        --------
        >>> await client.clan('#2P8QU22L2')
        #TODO: examples
        """

        shaped_tag = utils.shape_tag(tag)
        clan_data = await api.make_request(
            self.__session, api.Methods.CLAN(clantag=shaped_tag)
        )

        member_tags = [member["tag"] for member in clan_data["member_list"]]
        clan_data["member_list"] = member_tags

        clan_data["war"] = {}
        clan_data["war"]["wins"] = clan_data.pop("war_wins")
        clan_data["war"]["losses"] = clan_data.pop("war_losses")
        clan_data["war"]["ties"] = clan_data.pop("war_ties")
        clan_data["war"]["winstreak"] = clan_data.pop("war_win_streak")
        clan_data["war"]["frequency"] = clan_data.pop("war_frequency")
        clan_data["war"]["is_war_log_public"] = clan_data.pop("is_war_log_public")
        clan_data["war"]["league"] = clan_data.pop("war_league")

        if clan_data["war"]["is_war_log_public"]:
            returned_war_data = await asyncio.gather(
                api.make_request(
                    self.__session, api.Methods.CLAN_CURRENT_WAR(clantag=shaped_tag)
                ),
                api.make_request(
                    self.__session, api.Methods.CLAN_WARLOG(clantag=shaped_tag)
                ),
            )
            war_data, war_log_data = returned_war_data
            war_state = war_data["state"]

            clan_data["war"]["state"] = war_state
            clan_data["war"]["log"] = war_log_data["items"]

            if war_state != "notInWar":
                clan_data["war"]["currentwar"] = war_data

        clan_object = dacite.from_dict(
            data_class=Clan,
            data=clan_data,
            config=dacite.config.Config(type_hooks={str: utils.rawtime_to_datetime}),
        )
        return clan_object

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

        Examples
        --------
        >>> await client.player('...')
        #TODO: examples
        """

        shaped_tag = utils.shape_tag(tag)
        player_data = await api.make_request(
            self.__session, api.Methods.PLAYER(playertag=shaped_tag)
        )
        player_data["clan"] = player_data["clan"]["tag"]

        player_object = dacite.from_dict(data_class=Player, data=player_data)
        return player_object

    async def clan_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
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

        Examples
        --------
        >>> await client.aclan_rankings('russia')
        >>> await client.aclan_rankings('ru')
        #TODO: examples
        """

        loc = await self.get_location(location)
        rankings_data = await api.make_request(
            self.__session, api.Methods.CLAN_RANKINGS(location_id=loc.id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def player_rankings(self, location: LocationName | CountryCode) -> List[Tag]:
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

        Examples
        --------
        >>> await client.player_rankings('russia')
        >>> await client.player_rankings('ru')
        #TODO: examples
        """

        loc = await self.get_location(location)
        rankings_data = await api.make_request(
            self.__session, api.Methods.PLAYER_RANKINGS(location_id=loc.id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def clan_versus_rankings(
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

        Examples
        --------
        >>> await client.aclan_versus_rankings('russia')
        >>> await client.aclan_versus_rankings('ru')
        #TODO: examples
        """

        loc = await self.get_location(location)
        rankings_data = await api.make_request(
            self.__session, api.Methods.CLAN_VERSUS_RANKINGS(location_id=loc.id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def player_versus_rankings(
        self, location: LocationName | CountryCode
    ) -> List[Tag]:
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

        Examples
        --------
        >>> await client.aplayer_versus_rankings('russia')
        >>> await client.aplayer_versus_rankings('ru')
        #TODO: examples
        """

        loc = await self.get_location(location)
        rankings_data = await api.make_request(
            self.__session, api.Methods.PLAYER_VERSUS_RANKINGS(location_id=loc.id)
        )

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def goldpass(self) -> GoldPass:
        """
        Get information about the current gold pass season

        Returns
        -------
        GoldPass
            Gold pass object.

        Examples
        --------
        >>> await client.goldpass()
        #TODO: examples
        """

        goldpass_data = await api.make_request(self.__session, api.Methods.GOLDPASS())

        goldpass_object = dacite.from_dict(
            data_class=GoldPass,
            data=goldpass_data,
            config=dacite.config.Config(type_hooks={str: utils.rawtime_to_datetime}),
        )
        return goldpass_object

    async def all_locations(self):
        """
        List all locations.

        Returns
        -------
        dict
            dict with key, value pairs like `str`: ``Location``.
            Key can either be a location name or country code

        Examples
        --------
        >>> locations = await client.all_locations()
        >>> assert locations['ru'] == locations['russia']
        >>> print(locations['ru']) # however, is is not recommended, use ``client.get_location`` instead
        # TODO: Location(...)
        """

        if not hasattr(self, "_locations"):
            await self._init_locations()
        return self._locations

    async def get_location(self, location_name: LocationName | CountryCode):
        """
        Get location information

        Parameters
        ----------
        location_name : str
            Location name or country code

        Returns
        -------
        ``Location``

        Examples
        --------
        >>> location1 = await client.get_location('rU')
        >>> location2 = await client.get_location('ruSSia')
        >>> assert location1.id == location2.id

        >>> location3 = await client.get_location('kenya')
        >>> print(location3.id, location3.country_code)
        # TODO: ...
        """

        locations_mapping = await self.all_locations()
        name = location_name.lower()
        loc = locations_mapping.get(name)
        if loc is None:
            raise UnknownLocationError(loc)
        return loc

    async def all_clan_labels(self):
        """
        List clan labels

        Returns
        -------
        dict
            dict with key, value pairs like `str`: ``ClanLabel``.

        Examples
        --------
        >>> labels = await client.all_clan_labels()
        >>> print(labels['clan wars']) # however, is is not recommended, use ``client.get_clan_label`` instead
        # TODO: ClanLabel(...)
        """

        if not hasattr(self, "_clan_labels"):
            await self._init_clan_labels()
        return self._clan_labels

    async def get_clan_label(self, label_name: str):
        """
        Get clan label information

        Parameters
        ----------
        label_name : str
            Label name

        Returns
        -------
        ``ClanLabel``

        Examples
        --------
        >>> label = await client.get_clan_label('clAn Wars')
        >>> print(label.id, label.name)
        # TODO: ...
        """

        labels_mapping = await self.all_clan_labels()
        name = label_name.lower()
        label = labels_mapping.get(name)
        if label is None:
            raise UnknownClanLabelError(label)
        return label

    async def all_clan_leagues(self):
        """
        List clan leagues

        Returns
        -------
        dict
            dict with key, value pairs like `str`: ``ClanLeague``.

        Examples
        --------
        >>> leagues = await client.all_clan_leagues()
        >>> print(leagues['international']) # however, it is not recommended, use ``client.get_clan_league`` instead
        # TODO: League(...)
        """

        if not hasattr(self, "_clan_leagues"):
            await self._init_clan_leagues()
        return self._clan_leagues

    async def get_clan_league(self, league_name: str):
        """
        Get information about clan league

        Parameters
        ----------
        league_name : str
            League name

        Returns
        -------
        ``ClanLeague``

        Examples
        --------
        >>> league = await client.get_clan_league('international')
        >>> print(league.id, league.name)
        # TODO: ...
        """

        leagues_mapping = await self.all_clan_leagues()
        name = league_name.lower()
        league = leagues_mapping.get(name)
        if league is None:
            raise ValueError
        return league

    async def all_player_labels(self):
        """
        List player labels

        Returns
        -------
        dict
            dict with key, value pairs like `str`: ``PlayerLabel``.

        Examples
        --------
        >>> labels = await client.all_player_labels()
        >>> print(labels['...']) # however, it is not recommended, use ``client.get_player_label`` instead
        # TODO: PlayerLabel(...)
        """

        if not hasattr(self, "_player_labels"):
            await self._init_player_labels()
        return self._player_labels

    async def get_player_label(self, label_name: str):
        """
        Get player label information

        Parameters
        ----------
        label_name : str
            Label name

        Returns
        -------
        ``PlayerLabel``

        Examples
        --------
        >>> label = await client.get_player_label('...')
        >>> print(label.id, label.name)
        # TODO: ...
        """

        labels_mapping = await self.all_player_labels()
        name = label_name.lower()
        label = labels_mapping.get(name)
        if label is None:
            raise ValueError
        return label

    async def all_player_leagues(self):
        """
        List player leagues

        Returns
        -------
        ``PlayerLeague``

        Examples
        --------
        >>> leagues = await client.all_player_leagues()
        >>> print(leagues['...']) # not recommended, use ``client.get_player_league`` instead
        # TODO: League(...)
        """

        if not hasattr(self, "_player_leagues"):
            await self._init_player_leagues()
        return self._player_leagues

    async def get_player_league(self, league_name: str):
        """
        Get information about player league

        Parameters
        ----------
        league_name : str
            League name

        Returns
        -------
        ``PlayerLeague``

        Examples
        --------
        >>> league = await client.get_player_league('...')
        >>> print(league.id, league.name)
        # TODO: ...
        """

        leagues_mapping = await self.all_player_leagues()
        name = league_name.lower()
        league = leagues_mapping.get(name)
        if league is None:
            raise ValueError
        return league
