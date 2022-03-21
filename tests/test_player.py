import asyncio

from . import default_client


def test_player_primary(default_client):
    player = default_client.player("#LJJOUY2U8")
    assert player.name == "bone_appettit"


def test_player_tag_variety_primary(default_client):
    player1, player2, player3 = default_client._event_loop.run_until_complete(
        asyncio.gather(
            default_client._player("#LJJOUY2U8"),
            default_client._player("LJJOUY2U8"),
            default_client._player("ljjOUY2u8"),
        )
    )
    assert player1.name == player2.name == player3.name
