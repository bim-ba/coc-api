import asyncio

from . import default_client


def test_player_rankings_primary(default_client):
    players = default_client.player_rankings("russia")
    assert len(players) > 0


def test_player_rankings_location_variety_primary(default_client):
    players1, players2 = default_client._event_loop.run_until_complete(
        asyncio.gather(
            default_client._player_rankings("ruSSia"),
            default_client._player_rankings("ru"),
        )
    )
    assert len(players1) > 0
    assert len(players2) > 0
