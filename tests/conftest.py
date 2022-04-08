# type: ignore
# pylint: disable-all

import pytest

import pytest_asyncio

from cocapi import Client


def pytest_addoption(parser, pluginmanager):
    parser.addini("token", type="string", help="Your API token")


def pytest_sessionstart(session):
    token = session.config.getini("token")
    if not token:
        pytest.exit("Client API token was not provided!")


@pytest.fixture
def token(pytestconfig):
    token = pytestconfig.getini("token")
    return token


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def default_client(token):
    client = Client(token)
    yield client
    await client.close_session()
