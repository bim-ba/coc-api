import asyncio

import pytest

from cocapi.client import Client
from . import default_client, slow_down_requests

@pytest.mark.asyncio
async def test_goldpass_primary(default_client: Client, slow_down_requests):
    goldpass = await default_client.goldpass()
    assert goldpass.startTime.year > 2000
    assert goldpass.startTime.year > 2000
