import asyncio

import pytest

from cocapi.client import Client
from . import default_client, slow_down_requests

@pytest.mark.asyncio
async def test_player_rankings_primary(default_client: Client, slow_down_requests):
    players = await default_client.player_rankings('russia')
    assert len(players) > 0

@pytest.mark.asyncio
async def test_player_rankings_location_variety_primary(default_client: Client, slow_down_requests):
    players1, players2 = await asyncio.gather(
        default_client.player_rankings('ruSSia'),
        default_client.player_rankings('ru')
    )
    assert len(players1) > 0
    assert len(players2) > 0
