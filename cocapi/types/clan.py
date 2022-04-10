from typing import Any, Optional, List
from datetime import datetime

from pydantic import Field, validator

from .base import DefaultBaseModel
from .base_shared import BaseLabel, BaseLeague
from .badges import BadgeURLs
from .location import Location
from .aliases import (
    Tag,
    CaseInsensitiveStr,
    ClanType,
    ClanWarState,
    ClanWarActualResult,
    ClanWarFrequency,
)
from .. import utils


class ClanLabel(BaseLabel):
    pass


class ClanWarLeague(BaseLeague):
    pass


class ClanChatLanguage(DefaultBaseModel, anystr_lower=True):
    id: int
    name: CaseInsensitiveStr
    language_code: CaseInsensitiveStr


class ClanWarAttack(DefaultBaseModel):
    stars: int
    order: int
    duration: int
    attacker_tag: Tag
    defender_tag: Tag
    destruction_percentage: float


class ClanWarPlayer(DefaultBaseModel):
    tag: Tag
    map_position: int
    opponent_attacks: int
    attacks: Optional[List[ClanWarAttack]]
    best_opponent_attack: Optional[ClanWarAttack]


class ClanWarInfoClan(DefaultBaseModel):
    stars: int
    clan_level: int
    attacks: Optional[int]
    destruction_percentage: float
    members: Optional[List[ClanWarPlayer]]


class ClanWarInfo(DefaultBaseModel):
    clan: ClanWarInfoClan
    opponent: ClanWarInfoClan
    team_size: Optional[int]
    attacks_per_member: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    preparation_start_time: Optional[datetime]

    @validator("start_time", "end_time", "preparation_start_time", pre=True)
    def parse_datetime(cls: Any, value: Any):  # pylint: disable=no-self-argument
        if isinstance(value, str):
            fmt = "%Y%m%dT%H%M%S.%fZ"
            return datetime.strptime(value, fmt)
        return value


class ClanWarResult(DefaultBaseModel):
    result: Optional[ClanWarActualResult]
    clan: ClanWarInfoClan
    opponent: ClanWarInfoClan
    team_size: int
    attacks_per_member: int
    end_time: datetime

    @validator("end_time", pre=True)
    def parse_datetime(cls: Any, value: Any):  # pylint: disable=no-self-argument
        if isinstance(value, str):
            fmt = "%Y%m%dT%H%M%S.%fZ"
            return datetime.strptime(value, fmt)
        return value


class ClanWar(
    DefaultBaseModel,
    alias_generator=lambda field_name: f"war{utils.toCamel(field_name, lower_first=False)}",  # type: ignore
):
    wins: int
    losses: int
    ties: int
    win_streak: int
    is_war_log_public: bool = Field(alias="isWarLogPublic")
    league: ClanWarLeague
    frequency: ClanWarFrequency
    state: Optional[ClanWarState]
    currentwar: Optional[ClanWarInfo]
    log: Optional[List[ClanWarResult]]


class Clan(DefaultBaseModel):
    tag: Tag
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
