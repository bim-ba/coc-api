from typing import Any, Dict
import asyncio

import aiohttp

from . import api


class BaseClient:
    _token: str
    _session: aiohttp.ClientSession | None
    _session_headers: Dict[Any, Any]

    def __init__(self, token: str):
        self._token = token
        self._session = None
        self._session_headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
        }

    async def get_new_sesion(self):
        return aiohttp.ClientSession(headers=self._session_headers)

    async def get_session(self):
        if self._session is None:
            self._session = await self.get_new_sesion()
        return self._session

    async def close_session(self):
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        if self._session:
            await self._session.close()
            await asyncio.sleep(0)

    async def request(self, api_method: api.BaseMethod, **kwargs: Any):
        return await api.make_request(await self.get_session(), api_method, **kwargs)
