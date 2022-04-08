from typing import Optional, List

from .base import DefaultBaseModel
from .base_shared import BaseLeague, BaseLabel
from .aliases import Tag, Village, ClanRole, ClanWarPreference


class PlayerLeague(BaseLeague):
    pass


class PlayerLabel(BaseLabel):
    pass


class PlayerAchievment(DefaultBaseModel):
    name: str
    stars: int
    value: int
    target: int
    info: str
    village: Village
    completion_info: Optional[str]


class PlayerTroop(DefaultBaseModel):
    name: str
    level: int
    max_level: int
    village: Village
    super_troop_is_active: Optional[bool]


class Player(DefaultBaseModel):
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
