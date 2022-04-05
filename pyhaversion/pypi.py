"""pyhaversion package."""
from dataclasses import dataclass

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
from .exceptions import HaVersionInputException, HaVersionNotModifiedException

URL = "https://pypi.org/pypi/homeassistant/json"


@dataclass
class HaVersionPypi(HaVersionBase):
    """Handle versions for the PyPi source."""

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""
        if self.session is None:
            raise HaVersionInputException("Missing aiohttp.ClientSession")

    async def fetch(self, **kwargs):
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

        self._data = await request.json()

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data.get(DATA_INFO, {}).get(DATA_VERSION)

        versions = sorted(
            [
                AwesomeVersion(version)
                for version in self.data.get(DATA_RELEASES, [])
                if version.startswith("2")
            ],
            reverse=True,
        )
        for version in versions:
            if self.channel == HaVersionChannel.STABLE and version.beta:
                continue
            self._version = version
            break
