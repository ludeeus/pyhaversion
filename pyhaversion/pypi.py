"""pyhaversion package."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp.client import ClientTimeout
from aiohttp.hdrs import IF_NONE_MATCH
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import (
    DATA_INFO,
    DATA_RELEASES,
    DATA_VERSION,
    DEFAULT_HEADERS,
    HaVersionChannel,
)
from .exceptions import HaVersionNotModifiedException

URL = "https://pypi.org/pypi/homeassistant/json"


@dataclass
class HaVersionPypi(HaVersionBase):
    """Handle versions for the PyPi source."""

    async def fetch(self, **kwargs) -> dict[str, Any]:
        """Logic to fetch new version data."""
        headers = DEFAULT_HEADERS
        if (etag := kwargs.get("etag")) is not None:
            headers[IF_NONE_MATCH] = f'W/"{etag}"'

        request = await self.session.get(
            url=URL,
            headers=headers,
            timeout=ClientTimeout(total=self.timeout),
        )
        self._etag = request.headers.get("etag")

        if request.status == 304:
            raise HaVersionNotModifiedException

        return await request.json()

    def parse(self, data: dict[str, Any]) -> None:
        """Logic to parse new version data."""
        if self.channel != HaVersionChannel.BETA:
            self._version = data.get(DATA_INFO, {}).get(DATA_VERSION)
            return

        self._version = AwesomeVersion(
            sorted(
                [version for version in data.get(DATA_RELEASES, []) if version.startswith("2")],
                reverse=True,
            )[0]
        )
