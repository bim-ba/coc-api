from typing import Annotated, Literal, Text

PositiveInt = Annotated[int, "positive integer"]
NegativeInt = Annotated[int, "negative integer"]
CaseSensitiveStr = Annotated[Text, "case sensitive string"]
CaseInsensitiveStr = Annotated[Text, "case insensitive string"]

Url = Annotated[Text, "url string"]
RelativeUrl = Annotated[Url, "relative url string"]
RequestMethod = Annotated[
    Literal[
        "GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"
    ],
    "request method",
]
Tag = Annotated[CaseInsensitiveStr, "clan or player tag"]
"""
starts with #, only digits and capital letters, len = 1-9\n
regex = r'#[1-9A-Z]{1,9}'
"""
ClanType = Literal["open", "closed", "inviteOnly"]
"""open | closed | inviteOnly"""
ClanRole = Literal["leader", "coLeader", "admin", "member"]
"""leader | coLeader | admin | member"""
ClanWarFrequency = Literal[
    "always",
    "moreThanOncePerWeek",
    "oncePerWeek",
    "lessThanOncePerWeek",
    "never",
    "unknown",
]
"""always | moreThanOncePerWeek | oncePerWeek | lessThanOncePerWeek | never | unknown"""
ClanWarPreference = Literal["in", "out"]
"""in | out"""
ClanWarResultL = Literal["win", "lose", "tie"]
"""win | loss | tie"""
ClanWarState = Literal["warEnded", "notInWar", "preparation", "inWar"]
"""notInWar | preparation | inWar"""
Village = Literal["home", "builderBase"]
"""home | builderBase"""
LocationName = CaseInsensitiveStr
"""Russia | Ukraine | United States | Afghanistan"""
CountryCode = CaseInsensitiveStr
"""RU | UA | US | AF"""
LabelID = PositiveInt
"""29000000 | 29000001 | 29000022"""
LabelName = CaseInsensitiveStr
"""SomeLabel | AnotherLabel | Legend Label"""
LeagueID = PositiveInt
"""39000000 | 39000001 | 39000022"""
LeagueName = CaseInsensitiveStr
"""Unranked | Bronze League III | Legend League"""
