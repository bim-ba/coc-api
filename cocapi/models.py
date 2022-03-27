from typing import Any, List, Optional
from datetime import datetime
from dataclasses import dataclass


from .aliases import (
    CaseInsensitiveStr,
    Tag,
    Url,
    Village,
    ClanRole,
    ClanType,
    ClanWarFrequency,
    ClanWarPreference,
    ClanWarResultL,
    ClanWarState,
)


@dataclass(frozen=True)
class BadgeURLs:
    small: Url
    medium: Url
    large: Optional[Url]


@dataclass(frozen=True)
class BaseLabel:
    id: int
    name: CaseInsensitiveStr
    icon_urls: BadgeURLs


@dataclass(frozen=True)
class BaseLeague:
    id: int
    name: CaseInsensitiveStr
    icon_urls: Optional[BadgeURLs]


@dataclass(frozen=True)
class Location:
    id: int
    is_country: bool
    name: CaseInsensitiveStr
    country_code: Optional[CaseInsensitiveStr]


@dataclass(frozen=True)
class ClanLabel(BaseLabel):
    pass


@dataclass(frozen=True)
class ClanWarLeague(BaseLeague):
    pass


@dataclass(frozen=True)
class ClanChatLanguage:
    id: int
    name: CaseInsensitiveStr
    language_code: CaseInsensitiveStr


@dataclass(frozen=True)
class ClanWarAttack:
    stars: int
    order: int
    duration: int
    attacker_tag: Tag
    defender_tag: Tag
    destruction_percentage: float


@dataclass(frozen=True)
class ClanWarPlayer:
    tag: Tag
    map_position: int
    opponent_attacks: int
    attacks: Optional[List[ClanWarAttack]]
    best_opponent_attack: Optional[ClanWarAttack]


@dataclass(frozen=True)
class ClanWarInfoClan:
    stars: int
    clan_level: int
    attacks: Optional[int]
    destruction_percentage: float
    members: Optional[List[ClanWarPlayer]]


@dataclass(frozen=True)
class ClanWarInfo:
    clan: ClanWarInfoClan
    opponent: ClanWarInfoClan
    team_size: Optional[int]
    attacks_per_member: Optional[int]
    start_time: Optional[datetime | str | Any]  # datetime
    end_time: Optional[datetime | str | Any]  # datetime
    preparation_start_time: Optional[datetime | str | Any]  # datetime


@dataclass(frozen=True)
class ClanWarResult:
    result: Optional[ClanWarResultL]
    clan: ClanWarInfoClan
    opponent: ClanWarInfoClan
    team_size: int
    attacks_per_member: int
    end_time: datetime | str | Any  # datetime


@dataclass(frozen=True)
class ClanWar:
    wins: int
    losses: int
    ties: int
    winstreak: int
    is_war_log_public: bool
    league: ClanWarLeague
    frequency: ClanWarFrequency
    state: Optional[ClanWarState]
    currentwar: Optional[ClanWarInfo]
    log: Optional[List[ClanWarResult]]


@dataclass(frozen=True)
class Clan:
    tag: str
    name: str
    type: ClanType
    description: str
    badge_urls: BadgeURLs
    required_trophies: int
    required_versus_trophies: int
    required_townhall_level: int
    labels: List[ClanLabel]
    clan_level: int
    clan_points: int
    clan_versus_points: int
    member_list: List[Tag]
    war: ClanWar
    location: Optional[Location]
    chat_language: Optional[ClanChatLanguage]


@dataclass(frozen=True)
class PlayerLeague(BaseLeague):
    pass


@dataclass(frozen=True)
class PlayerLabel(BaseLabel):
    pass


@dataclass(frozen=True)
class PlayerAchievment:
    name: str
    stars: int
    value: int
    target: int
    info: str
    village: Village
    completion_info: Optional[str]


@dataclass(frozen=True)
class PlayerTroop:
    name: str
    level: int
    max_level: int
    village: Village
    super_troop_is_active: Optional[bool]


@dataclass(frozen=True)
class Player:
    tag: str
    name: str
    town_hall_level: int
    builder_hall_level: int
    exp_level: int
    trophies: int
    best_trophies: int
    war_stars: int
    attack_wins: int
    defense_wins: int
    versus_trophies: int
    best_versus_trophies: int
    versus_battle_wins: int
    donations: int
    donations_received: int
    troops: List[PlayerTroop]
    heroes: List[PlayerTroop]
    spells: List[PlayerTroop]
    achievements: List[PlayerAchievment]
    league: Optional[PlayerLeague]
    clan: Optional[Tag]
    role: Optional[ClanRole]
    war_preference: Optional[ClanWarPreference]
    town_hall_weapon_level: Optional[int]


@dataclass(frozen=True)
class GoldPass:
    start_time: datetime | str | Any  # datetime
    end_time: datetime | str | Any  # datetime
