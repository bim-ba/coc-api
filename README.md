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
<p align="center">Asynchronous wrapper around <a href="https://developer.clashofclans.com/#/documentation">Clash of Clans API</a>.

# Getting started

## Basic usage

```py
import asyncio

from cocapi import Client

async def main():
    client = Client('TOKEN') # your token

    clans = await client.clans(name='bomb', location='ru', max_members=30)
    print(clans)
    # ['#2P8QU22L2', '#2PPYL9928', '#22GLLRQYY', ...]

    first_clan, second_clan, third_clan = await asyncio.gather(
        client.clan(clans[0]),
        client.clan(clans[1]),
        client.clan(clans[2])
    )

    print(first_clan.name, first_clan.location)
    # bomb Location(id=32000193, isCountry=true, name='russia', countryCode='ru')

    print(second_clan.required_trophies, second_clan.required_townhall_level)
    # 200 3

    print(third_clan.description)
    # просто клан 12+ без матов ну и всё

if __name__ == '__main__':
    asyncio.run(main())
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

## Dependencies

| Requirement | Version |
| :---------- | :------ |
| aiohttp | ^3.8.1 |
| dacite | ^1.6.0 |
| pyhumps | ^3.5.3 |
| pytest | _dev_. ^7.1.1 |
| pytest-asyncio | _dev_. ^0.18.2 |
| black | _dev_. ^22.1.0 |

# Contents

* [Getting started](#getting-started)
    * [Basic usage](#basic-usage)
    * [Installation](#installation)
    * [Dependencies](#dependencies)
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
        * [all_locations](#method-all-locations)
        * [get_location](#method-get-location)
        * [all_clan_labels](#method-all-clan-labels)
        * [get_clan_label](#method-get-clan-label)
        * [all_clan_leagues](#method-all-clan-leagues)
        * [get_clan_league](#method-get-clan-league)
        * [all_player_labels](#method-all-player-labels)
        * [get_player_label](#method-get-player-label)
        * [all_player_leagues](#method-all-player-leagues)
        * [get_player_league](#method-get-player-league)
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
        * [ClientRequestError](#exception-client-request-error)
        * [JSONContentTypeError](#exception-json-content-type-error)
        * [UnknownLocationError](#exception-unknown-location-error)
        * [UnknownClanLabelError](#exception-unknown-clan-label-error)
    * [Aliases](#aliases)
        * [Tag](#alias-tag)
        * [ClanType](#alias-clan-type)
        * [ClanRole](#alias-clan-role)
        * [ClanWarFrequency](#alias-clan-war-frequency)
        * [ClanWarPreference](#alias-clan-war-preference)
        * [ClanWarResultL](#alias-clan-war-result-l)
        * [ClanWarState](#alias-clan-war-state)
        * [Village](#alias-village)
* [API Completness](#api-completness)
* [TODO](#todo)

# General API documentation

## Methods

<h3 id="method-clans">clans</h3>

**At least one filtering criteria must be used**  
Use this method to query all clans by name and/or filtering the results using various criteria. If name is used as part of search, it is required to be at least three characters long. It is not possible to specify ordering for results so clients should not rely on any specific ordering as that may change in the future releases of the [API](https://developer.clashofclans.com/#/documentation).

Normally, method makes 1 request , but there are some exclusions:  
- If `location` parameter is not `None`, method can make 1 additional request in order to convert location name to its id.  
- If `labels` parameter is not `None`, method can make 1 additional request in order to convert label/labels name to its id/ids.

_So the maximum number of request this method can make is 3_

Returns list of clan tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| name | `str` | _optional_. Clan name. Must be at least 3 characters long |
| min_members | `int` | _optional_. Minimum clan members |
| max_members | `int` | _optional_. Maximum clan members |
| min_clan_points | `int` | _optional_. Minimum clan points |
| min_clan_level | `int` | _optional_. Minimum clan level |
| war_frequency | `'always'` \| `'moreThanOncePerWeek'` \| `'oncePerWeek'` \| `'lessThanOncePerWeek'` \| `'never'` \| `'unknown'` | _optional_. Clan war frequency |
| location | `str` | _optional_. Clan location. May be either country code or full location name (_e.g. Russia == RU_) |
| labels | `str` \| `list[str]` | _optional_. Clan label or labels |

Examples:
```py
>>> clans = await client.clans(location='ru', war_frequency='never')
>>> print(clans)
# ['#RLU20URV', '#RV9RCQV', '#2LVV8RCJJ', ...]
```

<h3 id="method-clan">clan</h3>

Get information about a single clan by clan tag.

Normally, method makes 1 request, but there are some exclusions:  
- If clan war log is public, method makes 2 additional requests to gather information about clan war state and clan war log.

Returns [Clan](#clan-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| tag | `str` | _required_. Clan tag |

Examples:
```py
>>> clan = await client.clan('#2P8QU22L2')
>>> print(clan.name, clan.location)
# bomb Location(id=32000193, isCountry=true, name='russia', countryCode='ru')
```

<h3 id="method-player">player</h3>

Get information about a single player by player tag.

Returns [Player](#player-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| tag | `str` | _required_. Player tag |

Examples:
```py
>>> player = await client.player('#LJJOUY2U8')
>>> print(player.name)
# bone_appettit
```

<h3 id="method-clan-rankings">clan_rankings</h3>

Get clan rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- Method can make 1 additional request in order to convert location name to its id.

Returns list of clan tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. Location name or country code |

Examples:
```py
>>> clans = await client.clan_rankings('ru')
>>> print(clans[0])
# TODO: ...
```

<h3 id="method-player-rankings">player_rankings</h3>

Get player rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- Method can make 1 additional request in order to convert location name to its id.

Returns list of player tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. Location name or country code |

Examples:
```py
>>> players = await client.player_rankings('ru')
>>> print(players[0])
# TODO: ...
```

<h3 id="method-clan-versus-rankings">clan_versus_rankings</h3>

Get clan versus rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- Method can make 1 additional request in order to convert location name to its id.

Returns list of clan tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. Location name or country code |

Examples:
```py
>>> clans = await client.clan_versus_rankings('ru')
>>> print(clans[0])
# TODO: ...
```

<h3 id="method-player-versus-rankings">player_versus_rankings</h3>

Get player versus rankings for a specific location.

Normally, this method makes 1 request, but there is some exclusion:
- Method can make 1 additional request in order to convert location name to its id.

Returns list of player tags.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location | `str` | _required_. Location name or country code |

Examples:
```py
>>> players = await client.player_versus_rankings('ru')
>>> print(players[0])
# TODO: ...
```

<h3 id="method-goldpass">goldpass</h3>

Get information about the current gold pass season.

Returns [GoldPass](#goldpass-model) model.

Examples:
```py
>>> goldpass = await client.goldpass()
>>> print(goldpass.startTime)
# TODO: ...
```

<h3 id="method-all-locations">all_locations</h3>

List locations.

Returns dictionary with `key`: `value` pairs like `LocationName` | `Country Code`: [`Location`](#location-model).

Examples:
```py
>>> locations = await client.all_locations()
>>> assert locations['ru'] == locations['russia']
>>> print(locations['ru']) # not recommended, use ``client.get_location`` instead
# TODO: Location(...)
```

<h3 id="method-get-location">get_location</h3>

Get location information.

Returns [Location](#location-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| location_name | `str` | _required_. Location name or country code |

Examples:
```py
>>> location1 = await client.get_location('rU')
>>> location2 = await client.get_location('ruSSia')
>>> assert location1.id == location2.id

>>> location3 = await client.get_location('kenya')
>>> print(location3.id, location3.country_code)
# TODO: ...
```

<h3 id="method-all-clan-labels">all_clan_labels</h3>

List clan labels.

Returns dictionary with `key`: `value` pairs like `str`: [`ClanLabel`](#clan-label-model).

Examples:
```py
>>> labels = await client.all_clan_labels()
>>> print(labels['clan wars']) # not recommended, use ``client.get_clan_label`` instead
# TODO: ClanLabel(...)
```

<h3 id="method-get-clan-label">get_clan_label</h3>

Get clan label information.

Returns [ClanLabel](#clan-label-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| label_name | `str` | _required_. Label name |

Examples:
```py
>>> label = await client.get_clan_label('clAn Wars')
>>> print(label.id, label.name)
# TODO: ...
```

<h3 id="method-all-clan-leagues">all_clan_leagues</h3>

List clan leagues.

Returns dictionary with `key`: `value` pairs like `str`: [`ClanLeague`](#clan-league-model).

Examples:
```py
>>> leagues = await client.all_clan_leagues()
>>> print(leagues['international']) # not recommended, use ``client.get_clan_league`` instead
# TODO: League(...)
```

<h3 id="method-get-clan-league">get_clan_league</h3>

Get information about clan league.

Returns [ClanLeague](#clan-league-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| league_name | `str` | _required_. League name |

Examples:
```py
>>> league = await client.get_clan_league('international')
>>> print(league.id, league.name)
# TODO: ...
```

<h3 id="method-all-player-labels">all_player_labels</h3>

List player labels.

Returns dictionary with `key`: `value` pairs like `str`: [`PlayerLabel`](#player-label-model).

Examples:
```py
>>> labels = await client.all_player_labels()
>>> print(labels['...']) # not recommended, use ``client.get_player_label`` instead
# TODO: PlayerLabel(...)
```

<h3 id="method-get-player-label">get_player_label</h3>

Get player label information.

Returns [PlayerLabel](#player-label-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| label_name | `str` | _required_. Label name |

Examples:
```py
>>> label = await client.get_player_label('...')
>>> print(label.id, label.name)
# TODO: ...
```

<h3 id="method-all-player-leagues">all_player_leagues</h3>

List player leagues.

Returns dictionary with `key`: `value` pairs like `str`: [`PlayerLeague`](#player-league-model).

Examples:
```py
>>> leagues = await client.all_player_leagues()
>>> print(leagues['...']) # not recommended, use ``client.get_player_league`` instead
# TODO: League(...)
```

<h3 id="method-get-player-league">get_player_league</h3>

Get information about player league.

Returns [PlayerLeague](#player-league-model) model.

| Parameter | Type | Description |
| :-------- | :--: | :---------- |
| league_name | `str` | _required_. League name |

Examples:
```py
>>> league = await client.get_player_league('...')
>>> print(league.id, league.name)
# TODO: ...
```

## Models

Models are corresponds to the original [Clash of Clans API Models](https://developer.clashofclans.com/#/documentation), **but with some changes**. I have made small of these models (comparing them to the original ones) due to the fact that I have undertaken a slightly different design of these models in order to simplify and unify them.  
**In code all models are readonly, you cant change its contents - only read.**

<h3 id="baselabel-model">Base Label</h3>

This model stores information about label id, name and [iconUrls](#badgeurls-model). This model is just a parent for [PlayerLabel](#player-label-model) and [ClanLabel](#clan-label-model). It will never be created directly.

| Field | Type | Description |
| :---- | :--: | :---------- |
| id | `str` | Field unique id |
| name | `str` | _case insensitive_. Field unique name |
| iconUrls | [`BadgeURLs`](#badgeurls-model) \| `None` | _optional_. Field icons, some labels dont have icons. `None` if label does not have icons |

```mermaid
graph TD;
    BaseLabel-->PlayerLabel;
    BaseLabel-->ClanLabel;
```

<h3 id="baseleague-model">Base League</h3>

This model stores information about league id, its name and [iconUrls](#badgeurls-model). There are 2 types of leagues: [playerLeague](#player-league-model) and [clanLeague](#clan-league-model)

| Field | Type | Description |
| :---- | :--: | :---------- |
| id | `str` | Field unique id |
| name | `str` | _case insensitive_. Field unique name |
| iconUrls | [`BadgeURLs`](#badgeurls-model) \| `None` | _optional_. Field icons, some leagues dont have icons. `None` if league does not have icons |

```mermaid
graph TD;
    BaseLeague-->PlayerLeague;
    BaseLeague-->ClanWarLeague;
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
| frequency | `'always'` \| `'moreThanOncePerWeek'` \| `'oncePerWeek'` \| `'lessThanOncePerWeek'` \| `'never'` \| `'unknown'` | Clan war frequency preference |
| state | [`ClanWarState`](#clan-war-state-model) \| `None` | Current war state. `None` if `self.isWarLogPublic` is `False` |
| currentwar | [`ClanWarInfo`](#clan-war-info-model) \| `None` | Information about current war. `None` if `self.isWarLogPublic` is `False` |
| log | [`ClanWarState`](#clan-war-state-model) \| `None` | War log. `None` if `self.isWarLogPublic` is `False` |

<h3 id="clan-label-model">ClanLabel</h3>

Clan label is clan label. See [BaseLabel](#baselabel-model).

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

Clan war league is war league of clan. See [BaseLeague](#baseleague-model).

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

<h3 id="client-request-error">ClientRequestError</h3>

Raises while something went wrong while making request.

| Field | Type | Description |
| :---- | :--: | :---------- |
| response | `aiohttp.ClientResponse` | Response from server |
| message | <details><summary>`str`</summary>````'Error while making request! Server returned {status_code} for {url}.'````</details> | _can be supplemented_. Detailed message on whats going on |

<h3 id="exception-json-content-type-error">JSONContentTypeError</h3>

Raises while fetching some resource with content that cannot be decoded into JSON.

| Field | Type | Description |
| :---- | :--: | :---------- |
| content_type | `str` | Resource content type |
| message | <details><summary>`str`</summary>````'aiohttp throws an error while decoding JSON from the request! Content type was {content_type}: {error}'````</details> | _constant_. Detailed message on whats going on |

<h3 id="exception-unknown-location-error">UnknownLocationError</h3>

Raises when you trying to pass unknown location to function parameters.

| Field | Type | Description |
| :---- | :--: | :---------- |
| location | `Any` | What did you pass |
| message | <details><summary>`str`</summary>````'Unknown location! To get available locations, check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block'````</details> | _constant_. Detailed message on whats going on |

<h3 id="exception-unknown-clan-label-error">UnknownClanLabelError</h4>

Raises when you trying to pass unknown clan label to function parameters.

| Field | Type | Description |
| :---- | :--: | :---------- |
| label | `Any` | What did you pass |
| message | <details><summary>`str`</summary>````'Unknown clan label! To get available clan labels, check `self._locations` or official API reference https://developer.clashofclans.com/#/documentation for "locations/locations" block'````</details> | _constant_. Detailed message on whats going on |

## Aliases

<h3 id="alias-tag">Tag</h3>

Represents clan tag or player tag.  
Starts with _#_, may have only digits and capital letters, length in range 1 to 9 (except _#_ symbol) _<-- unverified_  
Equivalent to `str`.

Must match `r'#[1-9A-Z]{1,9}'` regex, but in fact there is no check.

```py
Tag = str
```

<h3 id="alias-clan-type">ClanType</h3>

_constant_. Represents clan type.  

```py
ClanType = 'open' | 'closed' | 'inviteOnly'
```

<h3 id="alias-clan-role">ClanRole</h3>

_constant_. Represents player clan role.  

```py
ClanRole = 'leader' | 'coLeader' | 'admin' | 'member'
```

<h3 id="alias-clan-war-frequency">ClanWarFrequency</h3>

_constant_. Represents clan war frequency.

```py
ClanWarFrequency = 'always' | 'moreThanOncePerWeek' | 'oncePerWeek' | 'lessThanOncePerWeek' | 'never' | 'unknown'
```

<h3 id="alias-clan-war-preference">ClanWarPreference</h3>

_constant_. Represents clan war preference.

```py
ClanWarPreference = 'in' | 'out'
```

<h3 id="alias-clan-war-result-l">ClanWarResultL</h3>

_constant_. Represents clan war result.

```py
ClanWarResultL = 'win' | 'lost' | 'tie'
```

<h3 id="alias-clan-war-state">ClanWarState</h3>

_constant_. Represents current war state.

```py
ClanWarState = 'notInWar' | 'preparation' | 'inWar'
```

<h3 id="alias-village">Village</h3>

_constant_. Represents game village.

```py
Village = 'home' | 'builderBase'
```

# API Completness

According to the original [API](https://developer.clashofclans.com/#/documentation).

| Method | Path | Completness | Description |
| :----: | :--- | :---------: | :---------- |
| `GET` | `/clans` | :heavy_check_mark: ([clans](#method-clans)) | Search clans |
| `GET` | `/clans/{clanTag}` | :heavy_check_mark: ([clan](#method-clan)) | Get clan information |
| `GET` | `/clans/{clanTag}/members` | :heavy_check_mark: ([clan](#method-clan)) | List clan members |
| `GET` | `/clans/{clanTag}/warlog` | :heavy_check_mark: ([clan](#method-clan)) | Retrieve clans clan war log |
| `GET` | `/clans/{clanTag}/currentwar` | :heavy_check_mark: ([clan](#method-clan)) | Retrieve information about clans current war |
| `GET` | `/clans/{clanTag}/currentwar/leaguegroup` | :x: []() | Retrieve information about clans current clan war league group |
| `GET` | `/clanwarleagues/wars/{warTag}` | :x: []() | Retrieve information about individual clan war league war |
|||||
| `GET` | `/players/{playerTag}` | :heavy_check_mark: ([player](#method-player)) | Get player information |
| `POST` | `/players/{playerTag}/verifytoken` | :x: []() | Verify player API token that can be found from the game settings |
|||||
| `GET` | `/leagues` | :heavy_check_mark: ([all_player_leagues](#method-all-player-leagues)) | List leagues |
| `GET` | `/leagues/{leagueId}` | :heavy_check_mark: ([get_player_league](#method-get-player-league)) | Get league information |
| `GET` | `/leagues/{leagueId}/seasons` | :x: []() | Get league seasons |
| `GET` | `/leagues/{leagueId}/seasons/{seasonId}` | :x: []() | Get league season rankings |
| `GET` | `/warleagues` | :heavy_check_mark: ([all_clan_leagues](#method-all-clan-leagues)) | List war leagues |
| `GET` | `/warleagues/{leagueId}` | :heavy_check_mark: ([get_clan_league](#method-get-clan-league)) | Get war league information |
|||||
| `GET` | `/labels/players` | :heavy_check_mark: ([all_player_labels](#method-all-player-labels), [get_player_label](#method-get-player-label)) | List player labels |
| `GET` | `/labels/clans` | :heavy_check_mark: ([all_clan_labels](#method-all-clan-labels), [get_clan_label](#method-get-clan-label)) | List clan labels |
|||||
| `GET` | `/locations` | :heavy_check_mark: ([all_locations](#method-all-locations)) | List locations |
| `GET` | `/locations/{locationId}` | :heavy_check_mark: ([get_location](#method-get-location)) | Get location information |
| `GET` | `/locations/{locationId}/rankings/clans` | :heavy_check_mark: ([clan_rankings](#method-clan-rankings)) | Get clan rankings for specific location |
| `GET` | `/locations/{locationId}/rankings/players` | :heavy_check_mark: ([player_rankings](#method-player-rankings)) | Get player rankings for specific location |
| `GET` | `/locations/{locationId}/rankings/clans-versus` | :heavy_check_mark: ([clan_versus_rankings](#method-clan-versus-rankings)) | Get clan versus rankings for specific location |
| `GET` | `/locations/{locationId}/rankings/players-versus` | :heavy_check_mark: ([player_versus_rankings](#method-player-versus-rankings)) | Get player versus rankings for specific location |
|||||
| `GET` | `/goldpass/seasons/current` | :heavy_check_mark: ([goldpass](#method-goldpass)) | Get information about the current gold pass season |

# TODO

- [x] `tests.py`
    - [ ] Testing under _Python <=3.9_
- [ ] Pendulum instead of standard datetime (is it worth it?)
