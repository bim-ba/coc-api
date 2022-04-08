from typing import Literal

PositiveInt = int
NegativeInt = int
CaseSensitiveStr = str
CaseInsensitiveStr = str

Url = str
RelativeUrl = Url
RequestMethod = Literal[
    "GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"
]
Tag = str
"""
starts with #, only digits and capital letters, len = 1-9\n
regex = r'#[1-9A-Z]{1,9}'
"""
ClanType = Literal["open", "closed", "inviteOnly"]
ClanRole = Literal["leader", "coLeader", "admin", "member"]
ClanWarFrequency = Literal[
    "always",
    "moreThanOncePerWeek",
    "oncePerWeek",
    "lessThanOncePerWeek",
    "never",
    "unknown",
]
ClanWarPreference = Literal["in", "out"]
ClanWarActualResult = Literal["win", "lose", "tie"]
ClanWarState = Literal["warEnded", "notInWar", "preparation", "inWar"]
Village = Literal["home", "builderBase"]
LocationName = CaseInsensitiveStr
CountryCode = CaseInsensitiveStr
LabelID = PositiveInt
LabelName = CaseInsensitiveStr
LeagueID = PositiveInt
LeagueName = CaseInsensitiveStr
