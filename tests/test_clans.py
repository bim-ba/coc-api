import asyncio

import pytest

from cocapi.client import Client
from . import default_client, slow_down_requests

class TestPrimaryClans:
    @pytest.mark.asyncio
    async def test_clans_small(self, default_client: Client, slow_down_requests):
        clans = await default_client.clans(name='dababy', min_members=10, war_frequency='always')
        assert len(clans) > 0

    @pytest.mark.asyncio
    async def test_clans_medium(self, default_client: Client, slow_down_requests):
        clans = await default_client.clans(location='ru', labels='clan wars', war_frequency='always', min_members=30)
        assert len(clans) > 0

    @pytest.mark.asyncio
    async def test_clans_large(self, default_client: Client, slow_down_requests):
        clans = await default_client.clans(location='russia', labels=['clan wars', 'trophy pushing'], war_frequency='always', min_members=30)
        assert len(clans) > 0

class TestExtendedClans:
    @pytest.mark.asyncio
    async def test_clans_location_fullname(self, default_client: Client, slow_down_requests):
        clans1, clans2, clans3 = await asyncio.gather(
            default_client.clans(location='russia'),
            default_client.clans(location='RUSSIA'),
            default_client.clans(location='RUSsIa')
        )
        assert len(clans1) == len(clans2) == len(clans3)

    @pytest.mark.asyncio
    async def test_clans_location_country_code(self, default_client: Client, slow_down_requests):
        clans1, clans2, clans3 = await asyncio.gather(
            default_client.clans(location='us'),
            default_client.clans(location='Us'),
            default_client.clans(location='US')
        )
        assert len(clans1) == len(clans2) == len(clans3)
