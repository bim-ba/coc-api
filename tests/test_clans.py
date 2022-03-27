# type: ignore
# pylint: disable-all

import asyncio

from . import default_client


async def test_clans_small(default_client):
    clans = await default_client.clans(
        name="dababy", min_members=10, war_frequency="always"
    )
    assert len(clans) > 0


async def test_clans_medium(default_client):
    clans = await default_client.clans(
        location="ru", labels="clan wars", war_frequency="always", min_members=30
    )
    assert len(clans) > 0


async def test_clans_large(default_client):
    clans = await default_client.clans(
        location="russia",
        labels=["clan wars", "trophy pushing"],
        war_frequency="always",
        min_members=30,
    )
    assert len(clans) > 0


async def test_clans_location_fullname(default_client):
    clans1, clans2, clans3 = await asyncio.gather(
        default_client.clans(location="russia"),
        default_client.clans(location="RUSSIA"),
        default_client.clans(location="RUSsIa"),
    )
    assert len(clans1) == len(clans2) == len(clans3)


async def test_clans_location_country_code(default_client):
    clans1, clans2, clans3 = await asyncio.gather(
        default_client.clans(location="us"),
        default_client.clans(location="Us"),
        default_client.clans(location="US"),
    )
    assert len(clans1) == len(clans2) == len(clans3)
