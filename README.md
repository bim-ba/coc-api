<p align="center">
    <a href="" alt="Python">
        <img src="https://img.shields.io/badge/python-3.6 | 3.7 | 3.8 | 3.9 | 3.10-blue"/>
    </a>
    <a>
        <img src="https://img.shields.io/static/v1?label=code style&message=black&color=black"/>
    </a>
    <br/>
    <a href="" alt="Contributions">
        <img src="https://img.shields.io/badge/contributions-welcome-brightgreen">
    </a>
</p>

<h1 align="center">coc-api</h1>
<p align="center">Wrapper around <a href="https://developer.clashofclans.com/#/documentation">Clash of Clans API</a> implemented in Python.

# Getting started

## Basic usage

```python
from cocapi import Client

client = Client('TOKEN') # your token

clans = client.clans(name='bomb', location='ru', max_members=30)
print(clans)
# ['#2P8QU22L2', '#2PPYL9928', '#2PPYL9928', ...]

clan = client.clan(clans[0])
print(clan.name, clan.location)
# bomb Location(id=32000193, isCountry=true, name='russia', countryCode='ru')
```

## Installation

For now, you can install it only from source. This package will be available on PyPi
as soon as code will be good and there will be no errors, I think now it is only a raw version. For the main branch I am using a [poetry](https://python-poetry.org/) to manage the packages, but you can use whatever you want (there are `requirements.txt` and `dev-requirements.txt` for backward comatibility).

```shell
$ git clone https://github.com/bim-ba/coc-api.git
$ cd coc-api
$ poetry install --no-dev
```

If you want to contribute, you need to install some dev packages.

```shell
$ poetry install
```

## Requirements

| Requirement | Version |
| :---------- | :------ |
| aiohttp | ^3.8.1 |
| dacite | ^1.6.0 |
| pyhumps | ^3.5.3 |
| pytest | _dev_. ^7.1.1 |
| black | _dev_. ^22.1.0 |

# Contents

* [Getting started](#getting-started)
    * [Basic usage](#basic-usage)
    * [Installation](#installation)
    * [Requirements](#requirements)
* [General API Documentation](#general-api-documentation)
    * [Methods](#methods)
        * [clans](#method-clans)
        * [clan](#method-clan)
        * [player](#method-player)
        * [clan_rankings](#method-clan-rankings)
        * [player_rankings](#method-player-rankings)
        * [clan_versus_rankings](#method-clan-versus-rankings)
        * [player_versus_rankings](#method-player-versus-rankings)
        * [goldpass](#method-goldpass)
        * [_fetch](#method-__fetch__)
        * [_validate_response](#method-__validate_response__)
        * [_init_location_list](#method-__init_location_list__)
        * [_init_clan_labels_list](#method-__init_clan_labels_list__)
        * [_get_location_id](#method-__get_location_id__)
        * [_get_clan_label_id](#method-__get_clan_label_id__)
    * [Models](#models)
        * [Label](#label-model)
        * [League](#league-model)
        * [Location](#location-model)
        * [BadgeURLs](#badgeurls-model)
        * [Player](#player-model)
        * [PlayerLabel](#player-label-model)
        * [PlayerLeague](#player-league-model)
        * [PlayerAchievment](#player-achievment-model)
        * [PlayerTroop](#player-troop-model)
        * [Clan](#clan-model)
        * [ClanWar](#clan-war-model)
        * [ClanLabel](#clan-label-model)
        * [ClanWarInfo](#clan-war-info-model)
        * [ClanWarAttack](#clan-war-attack-model)
        * [ClanWarLeague](#clan-war-league-model)
        * [ClanWarPlayer](#clan-war-player-model)
        * [ClanWarResult](#clan-war-result-model)
        * [ClanWarInfoClan](#clan-war-info-clan-model)
        * [ClanChatLanguage](#clan-chat-language-model)
        * [GoldPass](#goldpass-model)
    * [Exceptions](#exceptions)
        * [UnknownLocationError](#exception-unknown-location-error)
        * [UnknownClanLabelError](#exception-unknown-clan-label-error)
    * [Aliases](#aliases)
        * [CaseSensitiveStr](#alias-case-sensitive-str)
        * [CaseInsensitiveStr](#alias-case-insensitive-str)
        * [PositiveInt](#alias-positive-int)
        * [Url](#alias-url)
        * [RelativeUrl](#alias-relative-url)
        * [Tag](#alias-tag)
        * [ClanType](#alias-clan-type)
        * [ClanRole](#alias-clan-role)
        * [ClanWarFrequency](#alias-clan-war-frequency)
        * [ClanWarPreference](#alias-clan-war-preference)
        * [ClanWarResultL](#alias-clan-war-result-l)
        * [ClanWarState](#alias-clan-war-state)
        * [Village](#alias-village)
        * [LocationName](#alias-location-name)
        * [CountryCode](#alias-country-code)
        * [LabelID](#alias-label-id)
        * [LabelName](#alias-label-name)
        * [LeagueID](#alias-league-id)
        * [LeagueName](#alias-league-name)
* [TODO](#todo)

# General API documentation

## Methods

<h3 id="method-clans">clans</h3>

**At least one filtering criteria must be used**  
Use this method to query all clans by name and/or filtering the results using various criteria. If name is used as part of search, it is required to be at least three characters long. It is not possible to specify ordering for results so clients should not rely on any specific ordering as that may change in the future releases of the [API](https://developer.clashofclans.com/#/documentation).

Normally, method makes 1 request , but there are some exclusions:  
- If `location` parameter is not `None`, method can make 1 additional request to [API](https://developer.clashofclans.com/#/documentation) in order to convert location name to its id. For details see [_get_location_id](#method-get-location-id).  
- If `labels` parameter is not `None`, method can make 1 additional request to [API](https://developer.clashofclans.com/#/documentation) in order to convert label/labels name to its id/ids. For details see [_get_clan_label_id](#method-get-clan-label-id).

_So the maximum number of request this method can make is 3_

Returns list of clan tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| name | `str` | _optional_. Clan name. Must be at least 3 characters long |
| min_members | `int` | _optional_. Minimum clan members |
| max_members | `int` | _optional_. Maximum clan members |
| min_clan_points | `int` | _optional_. Minimum clan points |
| min_clan_level | `int` | _optional_. Minimum clan level |
| war_frequency | `always` \| `moreThanOncePerWeek` \| `oncePerWeek` \| `lessThanOncePerWeek` \| `never` \| `'unknown'` | _optional_. Clan war frequency |
| location | `str` | _optional_. Clan location. May be either country code or full location name (_e.g. Russia == RU_) |
| labels | `str` \| `list[str]` | _optional_. Clan label or labels |

Examples:

```py
>>> clans = await client.clans(location='ru', war_frequency='never')
['#RLU20URV', '#RV9RCQV', '#2LVV8RCJJ', ...] # results may differ
```

<h3 id="method-clans">clan</h3>

Get information about a single clan by clan tag.

Normally, method makes 1 request, but there are some exclusions:  
- If clan war log is public, this method makes 2 additional requests to gather information about clan war state and clan war log.

Returns [Clan](#clan-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| tag | `str` | _required_. Clan tag. Tag can be in any form (_e.g. "AAAAAA" == "#AAAAAA" == "%23AAAAAA" == "aaaaaa"_) |

Examples:

```py
>>> clan1 = await client.clan('#2P8QU22L2')
>>> print(clan.name, clan.location)
# bomb Location(id=32000193, isCountry=true, name='russia', countryCode='ru')
>>> clan2 = await client.clan('2P8QU22L2')
>>> clan3 = await client.clan('%232P8QU22L2')
>>> assert clan1 == clan2 == clan3
```

<h3 id="method-player">player</h3>

Get information about a single player by player tag.

This method makes only 1 request.

Returns [Player](#player-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| tag | `str` | _required_. _case insensitive_. Player tag. Tag can be in any form (_e.g. "AAAAAA" == "#AAAAAA" == "%23AAAAAA" == "aaaaaa"_) |

Examples:

```py
>>> player1 = await client.player('#LJJOUY2U8')
>>> print(player1.name) # results may differ
# bone_appettit
```

<h3 id="method-clan-rankings">clan_rankings</h3>

Get clan rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- See [_get_location_id](#method-get-location-id).

Returns list of clan tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. _case insentive_. Location name or country code |

Examples:

```py
>>> clans_in_russia = await client.clan_rankings('ru')
print(clans_in_russia[0]) # results may differ
# ...
```

<h3 id="method-player-rankings">player_rankings</h3>

Get player rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- See [_get_location_id](#method-get-location-id).

Returns list of player tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. _case insentive_. Location name or country code |

Examples:

```py
>>> players_in_russia = await client.player_rankings('ru')
print(players_in_russia[0]) # results may differ
# ...
```

<h3 id="method-clan-versus-rankings">clan_versus_rankings</h3>

Get clan versus rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- See [_get_location_id](#method-get-location-id).

Returns list of clan tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. _case insentive_. Location name or country code |

Examples:

```py
>>> clans_in_russia = await client.clan_versus_rankings('ru')
print(clans_in_russia[0]) # results may differ
# ...
```

<h3 id="method-player-versus-rankings">player_versus_rankings</h3>

Get player versus rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- See [_get_location_id](#method-get-location-id).

Returns list of player tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. _case insensitive_. Location name or country code |

Examples:

```py
>>> players_in_russia = await client.player_versus_rankings('ru')
print(players_in_russia[0]) # results may differ
# ...
```

<h3 id="method-goldpass">goldpass</h3>

Get information about the current gold pass season

This method always makes only 1 request.

Returns [GoldPass](#goldpass-model) model.

Examples:

```py
>>> goldpass = await client.goldpass()
>>> print(goldpass.startTime) # result may differ
# ...
```

## Models

Models are similar to the original [Clash of Clans API Models](https://developer.clashofclans.com/#/documentation), **but with some changes**. I have made small changes to the design of these models (comparing them to the original ones) due to the fact that I have undertaken a slightly different design of these models in order to simplify and unify them.  
**In code all models are readonly, you cant change its contents - only read.**

<h3 id="label-model">Label</h3>

This model stores information about label id, name and [iconUrls](#badgeurls-model). This model is just a parent for [PlayerLabel](#player-label-model) and [ClanLabel](#clan-label-model). It will never be created directly.

| Field | Type | Description |
| :---- | :--: | :---------- |
| id | `str` | Field unique id |
| name | `str` | _case insensitive_. Field unique name |
| iconUrls | [`BadgeURLs`](#badgeurls-model) \| `None` | _optional_. Field icons, some labels dont have icons. `None` if label does not have icons |

```mermaid
graph TD;
    Label-->PlayerLabel;
    Label-->ClanLabel;
```

<h3 id="league-model">League</h3>

This model stores information about league id, its name and [iconUrls](#badgeurls-model). There are 2 types of leagues: [playerLeague](#player-league-model) and [clanLeague](#clan-league-model)

| Field | Type | Description |
| :---- | :--: | :---------- |
| id | `str` | Field unique id |
| name | `str` | _case insensitive_. Field unique name |
| iconUrls | [`BadgeURLs`](#badgeurls-model) \| `None` | _optional_. Field icons, some leagues dont have icons. `None` if league does not have icons |

```mermaid
graph TD;
    League-->PlayerLeague;
    League-->ClanWarLeague;
```

<h3 id="location-model">Location</h3>

This model stores information about location id, its name and country code. Location is not always a country (e.g. _International_), thats why `isCountry` field is exist and `countryCode` may be `None`.

| Field | Type | Description |
| :---- | :--: | :---------- |
| id | `int` | Location unique id |
| name | `str` | _case insensitive_. Location unique name |
| isCountry | `bool` | `True` if location is country |
| countryCode | `str` \| `None` | _optional_. Location country code. `None` if location is not country |

<h3 id="badgeurls-model">BadgeURLs</h3>

This model stores information about small, medium and large image urls. Urls for some models may be missing, also a few models can have missing fields, thats why it is either `str` or `None`.

| Field | Type | Description |
| :---- | :--: | :---------- |
| small | `str` \| `None` | _optional_. Small icon url. `None` if missing |
| medium | `str` \| `None` | _optional_. Medium icon url. `None` if missing |
| large | `str` \| `None` | _optional_. Large icon url. `None` if missing |

<h3 id="player-model">Player</h3>

This model describes all information about player.

| Field | Type | Description |
| :---- | :--: | :---------- |
| tag | `str` | Player unique tag |
| name | `str` | Player name |
| townHallLevel | `int` | Player townhall level |
| builderHallLevel | `int` | Player builder hall level |
| expLevel | `int` | Player experience |
| trophies | `int` | Player trophies |
| bestTrophies | `int` | Player best trophies |
| warStars | `int` | Player summary war stars |
| attackWins | `int` | Player summary attack wins |
| defenseWins | `int` | Player summary defense wins |
| versusTrophies | `int` | Player versus trophies (builder base) |
| bestVersusTrophies | `int` | Player best versus trophies (builder base) |
| versusBattleWins | `int` | Player summary versus battle wins |
| donations | `int` | Player summary donations |
| donationsReceived | `int` | Player summary donations received |
| troops | <code>list[[PlayerTroop](#player-troop-model)]</code> | Player troops leveling |
| heroes | <code>list[[PlayerTroop](#player-troop-model)]</code> | Player heroes leveling |
| spells | <code>list[[PlayerTroop](#player-troop-model)]</code> | Player spells leveling |
| league | [`PlayerLeague`](#player-league-model) \| `None` | _optional_. Player league. `None` if player does not have league |
| clan | `str` | _optional_. Clan tag. It is not [Clan](#clan-model) due to recursion and object weight. `None` if player does not have clan |
| role | `'leader'` \| `'coLeader'` \| `'admin'` \| `'member'` \| `None` | _optional_. Player role in clan. `None` if player does not have clan |
| warPreference | `'in'` \| `'out'` \| `None` | _optional_. Player war preference. `None` if player does not specify it |
| townHallWeaponLevel | `int` \| `None` | _optional_. Player town hall weapon level (it is unlocked for player from 13 townhall level). `None` if player town hall is less than 13 |

<h3 id="player-label-model">PlayerLabel</h3>

This model describes player label information. Inherited from [Label](#label-model).

<h3 id="player-league-model">PlayerLeague</h3>

This model describes player league information. Inherited from [League](#league-model).

<h3 id="player-achievment-model">PlayerAchievment</h3>

This model describes information about some player achievment.

| Field | Type | Description |
| :---- | :--: | :---------- |
| name | `str` | Achievment name |
| stars | `int` | How many stars player have in this achievment |
| value | `int` | Progress |
| target | `int` | How much is needed to go to the next star |
| info | `str` | Detailed information about this achievment |
| village | `'home'` \| `'builderBase'` | In what village it achievment can obtained be |
| completionInfo | `str` \| `None` | _optional_. Completion info. `None` if ... |

<h3 id="player-troop-model">PlayerTroop</h3>

This model describes information about player troops (troops/spells/heroes). **This is not describes cuurent troops in player army camp, this describes troops leveling.**  
_Sometimes i think i should call it PlayerItem_

| Field | Type | Description |
| :---- | :--: | :---------- |
| name | `str` | Troop name |
| level | `int` | Troop level |
| maxLevel | `int` | Max troop level to which it can be upgraded |
| village | `'home'` \| `'builderBase'` | Which village this warrior belongs to |
| superTroopIsActive | `bool` \| `None` | _optional_. `True` if player activated _Super Troop Potion_. `None` if troop can not be _Super_ (spells and heroes can not be in _super form_) |

<h3 id="clan-model">Clan</h3>

This model describes all information about clan.

| Field | Type | Description |
| :---- | :--: | :---------- |
| tag | `str` | Clan unique tag |
| name | `str` | Clan name |
| type | `'open'` \| `'closed'` \| `'inviteOnly'` | Clan type |
| description | `str` | Clan description |
| badgeUrls | [`BadgeURLs`](#badgeurls-model) | Clan icon urls |
| requiredTrophies | `int` | Required trophies to join this clan |
| requiredVersusTrophies | `int` | Required versus trophies (builder base) to join this clan |
| requiredTownhallLevel | `int` | Required town hall level to join this clan |
| labels | <code>list[[ClanLabel](#clan-label-model)]</code> | List of clan labels |
| clanLevel | `int` | Clan level |
| clanPoints | `int` | Clan points |
| clanVersusPoints | `int` | Clan versus points |
| memberList | `list[str]` | List of tags of clan members |
| war | [`ClanWar`](#clan-war-model) | Information about war |
| location | [`Location`](#location-model) \| `None` | _optional_. Information about clan location. `None` if clan did not specify it |
| chatLanguage | [`ClanChatLanguage`](#clan-chat-language-model) \| `None` | _optional_. Information about clan chat primary language. `None` if clan did not specify it |

<h3 id="clan-war-model">ClanWar</h3>

This model describes all summary information about clan war state. If `isWarLogPublic` is `False` you can not access current war information (including state) and war log.

| Field | Type | Description |
| :---- | :--: | :---------- |
| wins | `int` | How many times clan has won wars |
| losses | `int` | How many times clan has lost wars |
| ties | `int` | How many times clan has played a draw in wars |
| winstreak | `int` | War winstreak |
| isWarLogPublic | `bool` | `True` if clan war log is public |
| frequency | `always` \| `moreThanOncePerWeek` \| `oncePerWeek` \| `lessThanOncePerWeek` \| `never` \| `'unknown'` | Clan war frequency preference |
| state | [`ClanWarState`](#clan-war-state-model) \| `None` | Current war state. `None` if `self.isWarLogPublic` is `False` |
| currentwar | [`ClanWarInfo`](#clan-war-info-model) \| `None` | Information about current war. `None` if `self.isWarLogPublic` is `False` |
| log | [`ClanWarState`](#clan-war-state-model) \| `None` | War log. `None` if `self.isWarLogPublic` is `False` |

<h3 id="clan-label-model">ClanLabel</h3>

Clan label is clan label. See [Label](#label-model).

<h3 id="clan-war-info-model">ClanWarInfo</h3>

This model describes information about current war.

| Field | Type | Description |
| :---- | :--: | :---------- |
| clan | [`ClanWarInfoClan`](#clan-war-info-clan-model) | Current war information about this clan |
| opponent | [`ClanWarInfoClan`](#clan-war-info-clan-model) | Current war information about opponent clan |
| startTime | [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) \| `None` | _optional_. Current war start time (UTC). `None` if ...<br/>_pendulum may be good here_ |
| endTime | [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) \| `None` | _optional_. Current war end time (UTC). `None` if ...<br/>_pendulum may be good here_ |
| preparationStartTime | [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) \| `None` | _optional_. Current war preparation start time (UTC). `None` if ...<br/>_pendulum may be good here_ |
| teamSize | `int` \| `None` | _optional_. Clan team size in current war. `None` if ... |
| attacksPerMember | `int` \| `None` | _optional_. How many attacks one member can perform. `None` if ... |

<h3 id="clan-war-attack-model">ClanWarAttack</h3>

This model describes information about clan war attack. Every attack has attacker and defender, as for it, this model stores only attacker and defender tags, not full [Player](#player-model) because of recursion.

| Field | Type | Description |
| :---- | :--: | :---------- |
| attackerTag | `str` | Attacker tag |
| defenderTag | `str` | Defender tag |
| stars | `int` | How many stars attacker obtain |
| destructionPercentage | `float` | Destruction percentage in range 0.0 to 100% |
| order | `int` | Map position where attacked base is located |
| duration | [`datetime.timedelta`](https://docs.python.org/3/library/datetime.html#timedelta-objects) | How long did the attack last<br/>_pendulum may be good here_ |

<h3 id="clan-war-league-model">ClanWarLeague</h3>

Clan war league is war league of clan. See [League](#league-model).

<h3 id="clan-war-player-model">ClanWarPlayer</h3>

This model describes information about player in current clan war and his attacks (if made).

| Field | Type | Description |
| :---- | :--: | :---------- |
| tag | `str` | Player tag |
| mapPosition | `int` | Player map position |
| opponentAttacks | `int` | It seems to be `len(self.attacks)` |
| attacks | <code>list[[ClanWarAttack](#clan-war-attack-model)]</code> \| `None` | _optional_. Attacks against opponents. `None` if no were made |
| bestOpponentAttack | [`ClanWarAttack`](#clan-war-attack-model) \| `None` | _optional_. Best attack in `self.attacks`, based on stars and destruction percentage. `None` if no were made |

<h3 id="clan-war-result-model">ClanWarResult</h3>

This model describes result of clan war. Used in clan war logs.

| Field | Type | Description |
| :---- | :--: | :---------- |
| result | `'win'` \| `'lose'` \| `'tie'` | War result |
| endTime | [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) | When the war is ended (UTC).<br/>_pendulum may be good here_ |
| teamSize | `int` | War team size |
| attacksPerMember | `int` | How many attacks one member can perform |
| clan | [`ClanWarInfoClan`](#clan-war-info-clan-model) | War information about this clan |
| opponent | [`ClanWarInfoClan`](#clan-war-info-clan-model) | War information about opponent clan |

<h3 id="clan-war-info-clan-model">ClanWarInfoClan</h3>

This model describes information about some clan in war.

| Field | Type | Description |
| :---- | :--: | :---------- |
| clanLevel | `int` | Clan level |
| stars | `int` | Total stars received |
| destructionPercentage | `float` | Total destruction percentage |
| attacks | `int` \| `None` | _optional_. Total maded attacks. `None` if no were made |
| members | [`ClanWarPlayer`](#clan-war-player-model) \| `None` | _optional_. Participating clan members in war. `None` if there are no such |

<h3 id="clan-chat-language-model">ClanChatLanguage</h3>

Clan chat language stores information about primary clan chat language.

| Field | Type | Description |
| :---- | :--: | :---------- |
| id | `int` | Language unique id |
| name | `str` | _case insensitive_. Language unique name |
| languageCode | `str` | _case insensitive_. Language code (like country code) |

<h3 id="goldpass-model">GoldPass</h3>

This model describes information about current gold pass.

| Field | Type | Description |
| :---- | :--: | :---------- |
| startTime | [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) | Current season start time (UTC)<br/>_pendulum may be good here_ |
| endTime | [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) | Current season end time (UTC)<br/>_pendulum may be good here_ |

## Exceptions

<h3 id="exception-unknown-location-error">UnknownLocationError</h3>

[Raises](https://github.com/bim-ba/coc-api/blob/6e247bfa6a8ff3938712bc3c814785c0eda867c0/src/client.py#L231) when you trying to pass unknown location to function parameters.

| Field | Type | Description |
| :---- | :--: | :---------- |
| location | `Any` | What did you pass |
| message | <details><summary>`str`</summary>````'Unknown location! To get available locations, check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block'````</details> | _constant_. Detailed message on whats going on |

<h3 id="exception-unknown-clan-label-error">UnknownClanLabelError</h4>

[Raises](https://github.com/bim-ba/coc-api/blob/6e247bfa6a8ff3938712bc3c814785c0eda867c0/src/client.py#L279) when you trying to pass unknown clan label to function parameters.

| Field | Type | Description |
| :---- | :--: | :---------- |
| label | `Any` | What did you pass |
| message | <details><summary>`str`</summary>````'Unknown clan label! To get available clan labels, check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block'````</details> | _constant_. Detailed message on whats going on |

## Aliases

<h3 id="alias-case-sensitive-str">CaseSensitiveStr</h3>

Describes case sensitive string.  
Equivalent to `str`.

```py
CaseSensitiveStr = str
```

<h3 id="alias-case-insensitive-str">CaseInsensitiveStr</h3>

Describes case insensitive string.  
Equivalent to `str`.

```py
CaseInsensitiveStr = str
```

<h3 id="alias-positive-int">PositiveInt</h3>

Describes positive int.  
Equivalent to `int`.

```py
PositiveInt = int
```

<h3 id="alias-url">Url</h3>

Describes full url (_e.g. `https://example.com/`_).  
Equivalent to `str`.

```py
Url = str
```

<h3 id="alias-relative-url">RelativeUrl</h3>

Describes relative url (_e.g. `/api/v1`_)  
Equivalent to `str`.

```py
RelativeUrl = Url
```

<h3 id="alias-tag">Tag</h3>

Describes clan tag or player tag.  
Starts with _#_, may have only digits and capital letters, length in range 1 to 9 (except _#_ symbol) _<-- unverified_  
Equivalent to `str`.

Must match `r'#[1-9A-Z]{1,9}'` regex, but in fact there is no check.

```py
Tag = str
```

<h3 id="alias-clan-type">ClanType</h3>

_constant_. Describes clan type.  

```py
ClanType = 'open' | 'closed' | 'inviteOnly'
```

<h3 id="alias-clan-role">ClanRole</h3>

_constant_. Describes player clan role.  

```py
ClanRole = 'leader' | 'coLeader' | 'admin' | 'member'
```

<h3 id="alias-clan-war-frequency">ClanWarFrequency</h3>

_constant_. Describes clan war frequency.

```py
ClanWarFrequency = 'always' | 'moreThanOncePerWeek' | 'oncePerWeek' | 'lessThanOncePerWeek' | 'never' | 'unknown'
```

<h3 id="alias-clan-war-preference">ClanWarPreference</h3>

_constant_. Describes clan war preference.

```py
ClanWarPreference = 'in' | 'out'
```

<h3 id="alias-clan-war-result-l">ClanWarResultL</h3>

_constant_. Describes clan war result.

```py
ClanWarResultL = 'win' | 'lost' | 'tie'
```

<h3 id="alias-clan-war-state">ClanWarState</h3>

_constant_. Describes current war state.

```py
ClanWarState = 'notInWar' | 'preparation' | 'inWar'
```

<h3 id="alias-village">Village</h3>

_constant_. Describes game village.

```py
Village = 'home' | 'builderBase'
```

<h3 id="alias-location-name">LocationName</h3>

_[case insensitive](#alias-case-insensitive-str)_. Describes full location name. (_e.g. russia | united states_).  
Equivalent to `str`.

```py
LocationName = CaseInsensitiveStr
```

<h3 id="alias-country-code">CountryCode</h3>

_[case insensitive](#alias-case-insensitive-str)_. Describes location country code. (_e.g. ru | us_).  
Equivalent to `str`.

```py
CountryCode = CaseInsensitivestr
```

<h3 id="alias-label-id">LabelID</h3>

_[positive int](#alias-positive-int)_. Describes player or clan label id.  
Equivalent to `str`.

```py
LabelID = PositiveInt
```

<h3 id="alias-label-name">LabelName</h3>

_[case insensitive](#alias-case-insensitive-str)_. Describes player or clan label name.  
Equivalent to `str`.

```py
LabelName = CaseInsensitiveStr
```

<h3 id="alias-league-id">LeagueID</h3>

_[positive int](#alias-positive-int)_. Describes player or clan war league id.  
Equivalent to `str`.

```py
LeagueID = PositiveInt
```

<h3 id="alias-label-name">LeagueName</h3>

_[case insensitive](#alias-case-insensitive-str)_. Describes player or clan war league name.  
Equivalent to `str`.

```py
LeagueName = CaseInsensitiveStr
```

# TODO

- [x] Its own event loop for `Client`
- [x] `tests.py`
    - [ ] Testing under _Python <=3.9_
    - [ ] Test documentation (_primary/extended tests_)
- [x] Model fields must correspond to _snake_case_ syntax
- [ ] Pendulum instead of standard datetime (is it worth it?)
- [ ] Comparable [Location](#location-model) and [ClanChatLanguage](#clan-chat-language-model)
- [ ] Comparable [Player](#player-model) and [ClanWarPlayer](#clan-war-player-model)
- [ ] Comparable [Clans](#clan-model)
- [ ] Comparable [Player](#player-model)
- [ ] `asyncio.gather` for `clans` method