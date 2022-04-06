"""pyhaversion package."""
from dataclasses import dataclass
from json import JSONDecodeError

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

    async def fetch(self, **kwargs):
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
            self._data = await request.json()
        except JSONDecodeError as exception:
            raise HaVersionFetchException(
                f"Could not parse JSON from response - {exception}"
            ) from exception

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data.get(DATA_CURRENT_VERSION)
        self._version_data = {
            DATA_RELEASE_DATE: self.data.get(DATA_RELEASE_DATE),
            DATA_RELEASE_NOTES: self.data.get(DATA_RELEASE_NOTES),
            DATA_RELEASE_TITLE: self.data.get(DATA_RELEASE_TITLE),
            DATA_RELEASE_DESCRIPTION: self.data.get(DATA_RELEASE_DESCRIPTION),
        }
