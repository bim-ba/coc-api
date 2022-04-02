from abc import ABC

import aiohttp


class BaseClient(ABC):
    # private properties
    @property
    def _token(self) -> str:
        ...

    @property
    def _session(self) -> aiohttp.ClientSession:
        ...

    @property
    def _email(self) -> str:
        ...

    @property
    def _password(self) -> str:
        ...
