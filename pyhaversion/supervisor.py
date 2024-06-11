"""pyhaversion package."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp.client import ClientTimeout
from aiohttp.hdrs import IF_NONE_MATCH

from .base import HaVersionBase
from .consts import (
    DATA_AUDIO,
    DATA_BOARD,
    DATA_CLI,
    DATA_DNS,
    DATA_HASSOS,
    DATA_HOMEASSISTANT,
    DATA_IMAGE,
    DATA_MULTICAST,
    DATA_OBSERVER,
    DATA_OS,
    DATA_SUPERVISOR,
    DEFAULT_BOARD,
    DEFAULT_HEADERS,
    DEFAULT_IMAGE,
    LOGGER,
)
from .exceptions import HaVersionNotModifiedException

URL = "https://version.home-assistant.io/{channel}.json"


@dataclass
class HaVersionSupervisor(HaVersionBase):
    """Handle versions for the Supervisor source."""

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""
        super().validate_input()
        if self.image is None:
            self.image = DEFAULT_IMAGE

    async def fetch(self, **kwargs) -> dict[str, Any]:
        """Logic to fetch new version data."""
        headers = DEFAULT_HEADERS
        if (etag := kwargs.get("etag")) is not None:
            headers[IF_NONE_MATCH] = etag

        request = await self.session.get(
            url=URL.format(channel=self.channel),
            headers=headers,
            timeout=ClientTimeout(total=self.timeout),
        )
        self._etag = request.headers.get("Etag")

        if request.status == 304:
            raise HaVersionNotModifiedException

        return await request.json()

    def parse(self, data: dict[str, Any]) -> None:
        """Logic to parse new version data."""
        if self.image != DEFAULT_IMAGE and self.image not in data.get(DATA_HOMEASSISTANT, {}):
            LOGGER.warning("Image '%s' not found, using default '%s'", self.image, DEFAULT_IMAGE)
            self.image = DEFAULT_IMAGE
        self._version = data.get(DATA_HOMEASSISTANT, {}).get(self.image)
        if self.board != DEFAULT_BOARD and self.board not in data.get(DATA_HASSOS, {}):
            LOGGER.warning("Board '%s' not found, using default '%s'", self.board, DEFAULT_BOARD)
            self.board = DEFAULT_BOARD
        self._version_data = {
            DATA_AUDIO: data.get(DATA_AUDIO),
            DATA_BOARD: self.board,
            DATA_CLI: data.get(DATA_CLI),
            DATA_DNS: data.get(DATA_DNS),
            DATA_OS: data.get(DATA_HASSOS, {}).get(self.board),
            DATA_IMAGE: self.image,
            DATA_MULTICAST: data.get(DATA_MULTICAST),
            DATA_OBSERVER: data.get(DATA_OBSERVER),
            DATA_SUPERVISOR: data.get(DATA_SUPERVISOR),
        }
