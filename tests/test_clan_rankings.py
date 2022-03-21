import asyncio

from . import default_client


def test_clan_rankings_primary(default_client):
    clans = default_client.clan_rankings("russia")
    assert len(clans) > 0


def test_clan_rankings_location_variety_primary(default_client):
    clans1, clans2 = default_client._event_loop.run_until_complete(
        asyncio.gather(
            default_client._clan_rankings("ruSSia"), default_client._clan_rankings("ru")
        )
    )
    assert len(clans1) > 0
    assert len(clans2) > 0
