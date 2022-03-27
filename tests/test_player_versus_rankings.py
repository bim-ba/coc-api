# type: ignore
# pylint: disable-all

import asyncio

from . import default_client


async def test_player_versus_rankings(default_client):
    players = await default_client.player_versus_rankings("russia")
    assert len(players) > 0


async def test_player_versus_rankings_location_variety(default_client):
    players1, players2 = await asyncio.gather(
        default_client.player_versus_rankings("ruSSia"),
        default_client.player_versus_rankings("ru"),
    )
    assert len(players1) > 0
    assert len(players2) > 0
