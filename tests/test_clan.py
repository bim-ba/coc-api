# type: ignore
# pylint: disable-all

import asyncio


async def test_clan(default_client):
    clan = await default_client.clan("#LQGPL8LL")
    assert clan.tag == "#LQGPL8LL"
    assert clan.war.wins >= 100


async def test_clan_tag_variety(default_client):
    clan1, clan2 = await asyncio.gather(
        default_client.clan("#LQGPL8LL"),
        default_client.clan("#lqGPL8ll"),
    )
    assert clan1.tag == clan2.tag
