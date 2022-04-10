import asyncio
from typing import Optional

from . import api
from .. import utils
from ..types import (
    aliases,
    exceptions,
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

    # private attributes
    _locations: dict[str, Location]
    _clan_labels: dict[str, ClanLabel]
    _clan_leagues: dict[str, ClanWarLeague]
    _player_labels: dict[str, PlayerLabel]
    _player_leagues: dict[str, PlayerLeague]

    async def _get_locations(self):
        location_mapping = {}  # type: dict[str, Location]
        response = await self.request(api.Methods.LOCATIONS())
        location_data = await response.json()

        for data in location_data["items"]:
            location = Location(**data)

            if location.name:
                location_mapping[location.name] = location
            if location.country_code:
                location_mapping[location.country_code] = location

        return location_mapping

    async def _get_clan_labels(self):
        clan_labels_mapping = {}  # type: dict[str, ClanLabel]
        response = await self.request(api.Methods.CLAN_LABELS())
        clan_label_data = await response.json()

        for data in clan_label_data["items"]:
            clan_label = ClanLabel(**data)

            clan_labels_mapping[clan_label.name] = clan_label

        return clan_labels_mapping

    async def _get_clan_leagues(self):
        clan_leagues_mapping = {}  # type: dict[str, ClanWarLeague]
        response = await self.request(api.Methods.WARLEAGUES())
        clan_leagues_data = await response.json()

        for data in clan_leagues_data["items"]:
            clan_league = ClanWarLeague(**data)

            clan_leagues_mapping[clan_league.name] = clan_league

        return clan_leagues_mapping

    async def _get_player_labels(self):
        player_labels_mapping = {}  # type: dict[str, PlayerLabel]
        response = await self.request(api.Methods.WARLEAGUES())
        player_labels_data = await response.json()

        for data in player_labels_data["items"]:
            player_label = PlayerLabel(**data)

            player_labels_mapping[player_label.name] = player_label

        return player_labels_mapping

    async def _get_player_leagues(self):
        player_leagues_mapping = {}  # type: dict[str, PlayerLeague]
        response = await self.request(api.Methods.WARLEAGUES())
        player_leagues_data = await response.json()

        for data in player_leagues_data["items"]:
            player_league = PlayerLeague(**data)

            player_leagues_mapping[player_league.name] = player_league

        return player_leagues_mapping

    async def clans(
        self,
        *,
        name: Optional[str] = None,
        min_members: Optional[aliases.PositiveInt] = None,
        max_members: Optional[aliases.PositiveInt] = None,
        min_clan_points: Optional[aliases.PositiveInt] = None,
        min_clan_level: Optional[aliases.PositiveInt] = None,
        war_frequency: Optional[aliases.ClanWarFrequency] = None,
        location: Optional[aliases.LocationName | aliases.CountryCode] = None,
        labels: Optional[list[aliases.LabelName] | aliases.LabelName] = None,
    ) -> list[aliases.Tag]:
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
            if not isinstance(labels, list):
                labels = [labels]

            lab_ids = []  # type: list[int]

            for lab in labels:
                lab = lab.lower()
                clan_lab = await self.get_clan_label(lab)
                lab_ids.append(clan_lab.id)

            # [1, 2, 3] => "1,2,3"
            comma_separated_lab_ids = ",".join(map(str, lab_ids))
            params["labelIds"] = comma_separated_lab_ids

        response = await self.request(api.Methods.CLANS(), params=params)
        clans_data = await response.json()
        tag_list = [clan["tag"] for clan in clans_data["items"]]
        return tag_list

    async def clan(self, tag: aliases.Tag) -> Clan:
        """
        Get information about a single clan by clan tag.
        Clan tags can be found using clan search operation.
        Note that clan tags start with hash character '#'.

        Parameters
        ----------
        tag : str
            Clan tag.

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
        response = await self.request(api.Methods.CLAN(clantag=shaped_tag))
        clan_data = await response.json()

        member_tags = [member["tag"] for member in clan_data["memberList"]]
        clan_data["memberList"] = member_tags

        clan_data["war"] = {
            key: value
            for key, value in clan_data.items()
            if key
            in (
                "warWins",
                "warLosses",
                "warTies",
                "warWinStreak",
                "warFrequency",
                "warLeague",
                "isWarLogPublic",
            )
        }

        if clan_data["war"]["isWarLogPublic"]:
            war_response, warlog_response = await asyncio.gather(
                self.request(api.Methods.CLAN_CURRENT_WAR(clantag=shaped_tag)),
                self.request(api.Methods.CLAN_WARLOG(clantag=shaped_tag)),
            )
            war_data, war_log_data = await asyncio.gather(
                war_response.json(), warlog_response.json()
            )
            war_state = war_data["state"]

            clan_data["war"]["warState"] = war_state
            clan_data["war"]["warLog"] = war_log_data["items"]

            if war_state != "notInWar":
                clan_data["war"]["warCurrentwar"] = war_data

        clan_object = Clan(**clan_data)
        return clan_object

    async def player(self, tag: aliases.Tag) -> Player:
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
        response = await self.request(api.Methods.PLAYER(playertag=shaped_tag))
        player_data = await response.json()
        player_data["clan"] = player_data["clan"]["tag"]

        player_object = Player(**player_data)
        return player_object

    async def clan_rankings(
        self, location: aliases.LocationName | aliases.CountryCode
    ) -> list[aliases.Tag]:
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
        response = await self.request(api.Methods.CLAN_RANKINGS(location_id=loc.id))
        rankings_data = await response.json()

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def player_rankings(
        self, location: aliases.LocationName | aliases.CountryCode
    ) -> list[aliases.Tag]:
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
        response = await self.request(api.Methods.PLAYER_RANKINGS(location_id=loc.id))
        rankings_data = await response.json()

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def clan_versus_rankings(
        self, location: aliases.LocationName | aliases.CountryCode
    ) -> list[aliases.Tag]:
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
        response = await self.request(
            api.Methods.CLAN_VERSUS_RANKINGS(location_id=loc.id)
        )
        rankings_data = await response.json()

        tag_list = [clan["tag"] for clan in rankings_data["items"]]
        return tag_list

    async def player_versus_rankings(
        self, location: aliases.LocationName | aliases.CountryCode
    ) -> list[aliases.Tag]:
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
        response = await self.request(
            api.Methods.PLAYER_VERSUS_RANKINGS(location_id=loc.id)
        )
        rankings_data = await response.json()

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

        response = await self.request(api.Methods.GOLDPASS())
        goldpass_data = await response.json()

        goldpass_object = GoldPass(**goldpass_data)
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
            setattr(self, "_locations", await self._get_locations())
        return self._locations

    async def get_location(
        self, location_name: aliases.LocationName | aliases.CountryCode
    ):
        """
        Get location information

        Parameters
        ----------
        location_name : str
            Location name or country code

        Raises
        ------
        ``UnknownLocationError``

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
            raise exceptions.UnknownLocationError(location_name)
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
            setattr(self, "_clan_labels", await self._get_clan_labels())
        return self._clan_labels

    async def get_clan_label(self, label_name: str):
        """
        Get clan label information

        Parameters
        ----------
        label_name : str
            Label name

        Raises
        ------
        ``UnknownClanLabelError``

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
            raise exceptions.UnknownClanLabelError(label_name)
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
            setattr(self, "_clan_leagues", await self._get_clan_leagues())
        return self._clan_leagues

    async def get_clan_league(self, league_name: str):
        """
        Get information about clan league

        Parameters
        ----------
        league_name : str
            League name

        Raises
        ------
        ``UnknownClanLeagueError``

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
            raise exceptions.UnknownClanLeagueError(league_name)
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
            setattr(self, "_player_labels", await self._get_player_labels())
        return self._player_labels

    async def get_player_label(self, label_name: str):
        """
        Get player label information

        Parameters
        ----------
        label_name : str
            Label name

        Raises
        ------
        ``UnknownPlayerLabelError``

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
            raise exceptions.UnknownPlayerLabelError(label_name)
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
            setattr(self, "_player_leagues", await self._get_player_leagues())
        return self._player_leagues

    async def get_player_league(self, league_name: str):
        """
        Get information about player league

        Parameters
        ----------
        league_name : str
            League name

        Raises
        ------
        ``UnknownPlayerLeagueError``

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
            raise exceptions.UnknownPlayerLeagueError(league_name)
        return league
