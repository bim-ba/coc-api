import pytest

from cocapi import Client

TOKEN = ""


@pytest.fixture
def default_client():
    client = Client(TOKEN)
    yield client
