import asyncio

from . import default_client


def test_clan_primary(default_client):
    clan = default_client.clan("#LQGPL8LL")

    assert clan.tag == "#LQGPL8LL"
    assert clan.war.wins >= 100


def test_clan_tag_variety_primary(default_client):
    clan1, clan2, clan3 = default_client._event_loop.run_until_complete(
        asyncio.gather(
            default_client._clan("#LQGPL8LL"),
            default_client._clan("LQGPL8LL"),
            default_client._clan("lqGPL8ll"),
        )
    )

    assert clan1.tag == clan2.tag == clan3.tag
