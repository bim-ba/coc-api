from abc import ABC
from typing import Text

import aiohttp

from .aliases import Url


class BaseClient(ABC):
    # public properties
    @property
    def uri(self) -> Url:
        ...

    # private properties
    @property
    def _token(self) -> Text:
        ...

    @property
    def _session(self) -> aiohttp.ClientSession:
        ...
