import asyncio

import pytest

from cocapi.client import Client
from . import default_client, slow_down_requests

@pytest.mark.asyncio
async def test_clan_primary(default_client: Client, slow_down_requests):
    clan = await default_client.clan('#LQGPL8LL')
    assert clan.tag == '#LQGPL8LL'
    assert clan.war.wins >= 100
    assert clan.war.winstreak >= 1

@pytest.mark.asyncio
async def test_clan_tag_variety_primary(default_client: Client, slow_down_requests):
    clan1, clan2, clan3, clan4 = await asyncio.gather(
        default_client.clan('#LQGPL8LL'),
        default_client.clan('LQGPL8LL'),
        default_client.clan('%23LQGPL8LL'),
        default_client.clan('lqGPL8ll')
    )
    assert clan1.tag == clan2.tag == clan3.tag == clan4.tag
