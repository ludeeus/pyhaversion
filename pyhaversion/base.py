from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import aiohttp
from awesomeversion import AwesomeVersion

from .consts import (
    DATA_CHANNEL,
    DATA_SOURCE,
    DEFAULT_TIMEOUT,
    HaVersionChannel,
    HaVersionSource,
)
from .exceptions import HaVersionInputException


@dataclass
class HaVersionBase:
    """HaVersion base class."""

    source: HaVersionSource = HaVersionSource.DEFAULT

    channel: HaVersionChannel = HaVersionChannel.DEFAULT

    board: str | None = None
    image: str | None = None

    session: aiohttp.ClientSession | None = field(repr=False, default=None)
    timeout: int = field(repr=False, default=DEFAULT_TIMEOUT)

    _etag: str | None = None

    _version: AwesomeVersion | None = field(repr=False, default=None)
    _version_data: dict[str, Any] = field(repr=False, default_factory=dict)

    def __post_init__(self):
        self.validate_input()

    @property
    def etag(self) -> str | None:
        """Return the etag of the last request if any."""
        return self._etag

    @property
    def version(self) -> AwesomeVersion | None:
        """Return the version."""
        return AwesomeVersion(self._version) if self._version else None

    @property
    def version_data(self) -> dict[str, Any] | None:
        """Return extended version data for supported sources."""
        return {
            DATA_SOURCE: self.source,
            DATA_CHANNEL: self.channel,
            **self._version_data,
        }

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""
        if self.session is None:
            raise HaVersionInputException("Missing aiohttp.ClientSession")

    async def fetch(self, **kwargs) -> dict[str, Any]:
        """Logic to fetch new version data."""

    def parse(self, data: dict[str, Any]) -> None:
        """Logic to parse new version data."""
