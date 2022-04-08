# type: ignore
# pylint: disable-all

import asyncio


async def test_player(default_client):
    player = await default_client.player("#LJJOUY2U8")
    assert player.name == "bone_appettit"


async def test_player_tag_variety(default_client):
    player1, player2 = await asyncio.gather(
        default_client.player("#LJJOUY2U8"),
        default_client.player("#ljjOUY2u8"),
    )
    assert player1.name == player2.name
