import asyncio

import pytest

from cocapi.client import Client
from . import default_client, slow_down_requests

@pytest.mark.asyncio
async def test_player_primary(default_client: Client, slow_down_requests):
    player = await default_client.player('#LJJOUY2U8')
    assert player.name == 'bone_appettit'

@pytest.mark.asyncio
async def test_player_tag_variety_primary(default_client: Client, slow_down_requests):
    player1, player2, player3, player4 = await asyncio.gather(
        default_client.player('#LJJOUY2U8'),
        default_client.player('LJJOUY2U8'),
        default_client.player('%23LJJOUY2U8'),
        default_client.player('ljjOUY2u8')
    )
    assert player1.name == player2.name == player3.name == player4.name
