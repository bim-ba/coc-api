# type: ignore
# pylint: disable-all

import asyncio

from . import default_client


async def test_clan_versus_rankings(default_client):
    clans = await default_client.clan_versus_rankings("russia")
    assert len(clans) > 0


async def test_clan_versus_rankings_location_variety(default_client):
    clans1, clans2 = await asyncio.gather(
        default_client.clan_versus_rankings("ruSSia"),
        default_client.clan_versus_rankings("ru"),
    )
    assert len(clans1) > 0
    assert len(clans2) > 0
