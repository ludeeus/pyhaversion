"""pyhaversion package."""

from __future__ import annotations

from dataclasses import dataclass
from json import JSONDecodeError
from typing import Any

from aiohttp.client import ClientTimeout
from aiohttp.hdrs import IF_NONE_MATCH

from .base import HaVersionBase
from .consts import (
    DATA_CURRENT_VERSION,
    DATA_RELEASE_DATE,
    DATA_RELEASE_DESCRIPTION,
    DATA_RELEASE_NOTES,
    DATA_RELEASE_TITLE,
    DEFAULT_HEADERS,
)
from .exceptions import HaVersionFetchException, HaVersionNotModifiedException

URL = "https://www.home-assistant.io/version.json"


@dataclass
class HaVersionHaio(HaVersionBase):
    """Handle versions for the home-assistant.io source."""

    async def fetch(self, **kwargs) -> dict[str, Any]:
        """Logic to fetch new version data."""
        headers = DEFAULT_HEADERS
        if (etag := kwargs.get("etag")) is not None:
            headers[IF_NONE_MATCH] = etag

        request = await self.session.get(
            url=URL,
            headers=headers,
            timeout=ClientTimeout(total=self.timeout),
        )
        self._etag = request.headers.get("Etag")

        if request.status == 304:
            raise HaVersionNotModifiedException

        try:
            return await request.json()
        except JSONDecodeError as exception:
            raise HaVersionFetchException(
                f"Could not parse JSON from response - {exception}"
            ) from exception

    def parse(self, data: dict[str, Any]) -> None:
        """Logic to parse new version data."""
        self._version = data.get(DATA_CURRENT_VERSION)
        self._version_data = {
            DATA_RELEASE_DATE: data.get(DATA_RELEASE_DATE),
            DATA_RELEASE_NOTES: data.get(DATA_RELEASE_NOTES),
            DATA_RELEASE_TITLE: data.get(DATA_RELEASE_TITLE),
            DATA_RELEASE_DESCRIPTION: data.get(DATA_RELEASE_DESCRIPTION),
        }
