# type: ignore
# pylint: disable-all


async def test_goldpass(default_client):
    goldpass = await default_client.goldpass()
    assert goldpass.start_time.year > 2000
    assert goldpass.end_time.year > 2000
