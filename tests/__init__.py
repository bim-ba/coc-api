# type: ignore
# pylint: disable-all

import pytest

import pytest_asyncio

from cocapi import Client

TOKEN = ""

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def default_client():
    client = Client(TOKEN)
    yield client
    await client.close()
