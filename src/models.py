# pyright: strict

from datetime import datetime, timedelta
from typing import List, Optional
from attrs import frozen, field, converters

from . import utils
from .aliases import (
    CaseInsensitiveStr, Tag, Url, Village,
    ClanRole, ClanType, ClanWarFrequency, ClanWarPreference, ClanWarResultL, ClanWarState
)

@frozen
class BadgeURLs:
    small: Optional[Url] = None
    medium: Optional[Url] = None
    large: Optional[Url] = None

@frozen
class Label:
    id: int
    name: CaseInsensitiveStr = field(converter=str.lower)
    iconUrls: BadgeURLs

@frozen
class League:
    id: int
    name: CaseInsensitiveStr = field(converter=str.lower)
    iconUrls: Optional[BadgeURLs] = None

@frozen
class Location:
    id: int
    isCountry: bool
    name: CaseInsensitiveStr = field(converter=str.lower)
    countryCode: Optional[CaseInsensitiveStr] = field(default=None, converter=converters.optional(str.lower))

@frozen
class ClanLabel(Label):
    pass

@frozen
class ClanWarLeague(League):
    pass

@frozen
class ClanChatLanguage:
    id: int
    name: CaseInsensitiveStr = field(converter=str.lower)
    languageCode: CaseInsensitiveStr = field(converter=str.lower)

@frozen
class ClanWarAttack:
    attackerTag: Tag
    defenderTag: Tag
    stars: int
    destructionPercentage: float
    order: int
    duration: timedelta

@frozen
class ClanWarPlayer:
    tag: Tag
    mapPosition: int
    opponentAttacks: int
    attacks: Optional[List[ClanWarAttack]] = None
    bestOpponentAttack: Optional[ClanWarAttack] = None

@frozen
class ClanWarInfoClan:
    clanLevel: int
    stars: int
    destructionPercentage: int
    attacks: Optional[int] = None
    members: Optional[List[ClanWarPlayer]] = None

@frozen
class ClanWarInfo:
    clan: ClanWarInfoClan
    opponent: ClanWarInfoClan
    startTime: Optional[datetime] = field(default=None, converter=converters.optional(utils.rawtime_to_datetime))
    endTime: Optional[datetime] = field(default=None, converter=converters.optional(utils.rawtime_to_datetime))
    preparationStartTime: Optional[datetime] = field(default=None, converter=converters.optional(utils.rawtime_to_datetime))
    teamSize: Optional[int] = None
    attacksPerMember: Optional[int] = None

@frozen
class ClanWarResult:
    result: ClanWarResultL
    endTime: datetime = field(converter=utils.rawtime_to_datetime)
    teamSize: int
    attacksPerMember: int
    clan: ClanWarInfoClan
    opponent: ClanWarInfoClan

@frozen
class ClanWar:
    wins: int
    losses: int
    ties: int
    winstreak: int
    isWarLogPublic: bool
    league: ClanWarLeague
    frequency: ClanWarFrequency
    state: Optional[ClanWarState] = None
    currentwar: Optional[ClanWarInfo] = None
    log: Optional[List[ClanWarResult]] = None

@frozen
class Clan:
    tag: str
    name: str
    type: ClanType
    description: str
    badgeUrls: BadgeURLs
    requiredTrophies: int
    requiredVersusTrophies: int
    requiredTownhallLevel: int
    labels: List[ClanLabel]
    clanLevel: int
    clanPoints: int
    clanVersusPoints: int
    memberList: List[Tag]
    war: ClanWar
    location: Optional[Location] = None
    chatLanguage: Optional[ClanChatLanguage] = None

@frozen
class PlayerLeague(League):
    pass

@frozen
class PlayerLabel(Label):
    pass

@frozen
class PlayerAchievment:
    name: str
    stars: int
    value: int
    target: int
    info: str
    village: Village
    completionInfo: Optional[str] = None

@frozen
class PlayerTroop:
    name: str
    level: int
    maxLevel: int
    village: Village
    superTroopIsActive: Optional[bool] = None

@frozen
class Player:
    tag: str
    name: str
    townHallLevel: int
    builderHallLevel: int
    expLevel: int
    trophies: int
    bestTrophies: int
    warStars: int
    attackWins: int
    defenseWins: int
    builderHallLevel: int
    versusTrophies: int
    bestVersusTrophies: int
    versusBattleWins: int
    donations: int
    donationsReceived: int
    troops: List[PlayerTroop]
    heroes: List[PlayerTroop]
    spells: List[PlayerTroop]
    achievements: List[PlayerAchievment]
    league: Optional[PlayerLeague] = None
    clan: Optional[Tag] = None
    role: Optional[ClanRole] = None
    warPreference: Optional[ClanWarPreference] = None
    townHallWeaponLevel: Optional[int] = None

@frozen
class GoldPass:
    startTime: datetime = field(converter=utils.rawtime_to_datetime)
    endTime: datetime = field(converter=utils.rawtime_to_datetime)
