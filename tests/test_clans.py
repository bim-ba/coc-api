import asyncio

from . import default_client


class TestPrimaryClans:
    def test_clans_small(self, default_client):
        clans = default_client.clans(
            name="dababy", min_members=10, war_frequency="always"
        )
        assert len(clans) > 0

    def test_clans_medium(self, default_client):
        clans = default_client.clans(
            location="ru", labels="clan wars", war_frequency="always", min_members=30
        )
        assert len(clans) > 0

    def test_clans_large(self, default_client):
        clans = default_client.clans(
            location="russia",
            labels=["clan wars", "trophy pushing"],
            war_frequency="always",
            min_members=30,
        )
        assert len(clans) > 0


class TestExtendedClans:
    def test_clans_location_fullname(self, default_client):
        clans1, clans2, clans3 = default_client._event_loop.run_until_complete(
            asyncio.gather(
                default_client._clans(location="russia"),
                default_client._clans(location="RUSSIA"),
                default_client._clans(location="RUSsIa"),
            )
        )
        assert len(clans1) == len(clans2) == len(clans3)

    def test_clans_location_country_code(self, default_client):
        clans1, clans2, clans3 = default_client._event_loop.run_until_complete(
            asyncio.gather(
                default_client._clans(location="us"),
                default_client._clans(location="Us"),
                default_client._clans(location="US"),
            )
        )
        assert len(clans1) == len(clans2) == len(clans3)
