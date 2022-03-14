import asyncio

import pytest

from cocapi.client import Client
from . import default_client, slow_down_requests

@pytest.mark.asyncio
async def test_clan_versus_rankings_primary(default_client: Client, slow_down_requests):
    clans = await default_client.clan_versus_rankings('russia')
    assert len(clans) > 0

@pytest.mark.asyncio
async def test_clan_versus_rankings_location_variety_primary(default_client: Client, slow_down_requests):
    clans1, clans2 = await asyncio.gather(
        default_client.clan_versus_rankings('ruSSia'),
        default_client.clan_versus_rankings('ru')
    )
    assert len(clans1) > 0
    assert len(clans2) > 0
