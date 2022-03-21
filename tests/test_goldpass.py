from . import default_client


def test_goldpass_primary(default_client):
    goldpass = default_client.goldpass()
    assert goldpass.start_time.year > 2000
    assert goldpass.start_time.year > 2000
