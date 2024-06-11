"""pyhaversion package."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp.client import ClientTimeout
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import DEFAULT_HEADERS, HaVersionChannel
from .exceptions import HaVersionFetchException

URL = "https://registry.hub.docker.com/v2/repositories/homeassistant/home-assistant/tags"


@dataclass
class HaVersionContainer(HaVersionBase):
    """Handle versions for the Container source."""

    async def fetch(self, **kwargs) -> dict[str, Any]:
        """Logic to fetch new version data."""
        request = await self.session.get(
            url=kwargs.get("url", URL),
            headers=DEFAULT_HEADERS,
            timeout=ClientTimeout(total=self.timeout),
        )
        data = await request.json()
        try:
            self.parse(data)
        except KeyError as exception:
            raise HaVersionFetchException(
                "Could not handle response from Docker Hub"
            ) from exception

        if not self.version and (next_url := data.get("next")):
            return await self.fetch(**{"url": next_url})

        return data

    def parse(self, data: dict[str, Any]) -> None:
        """Logic to parse new version data."""
        for image in data["results"]:
            if not (version := image["name"]).startswith("2"):
                continue
            if not len(version.split(".")) >= 3:
                continue

            version = AwesomeVersion(version)
            if version.dev:
                if self.channel == HaVersionChannel.DEV:
                    self._version = version
                    break
            elif version.beta:
                if self.channel == HaVersionChannel.BETA:
                    self._version = version
                    break
            else:
                self._version = version
                break
