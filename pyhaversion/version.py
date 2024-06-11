"""Get the latest Home Assistant version from various sources."""

from __future__ import annotations

import asyncio
from socket import gaierror
from typing import Any

from aiohttp import ClientError, ClientSession
from awesomeversion import AwesomeVersion

from .base import HaVersionBase
from .consts import (
    DEFAULT_BOARD,
    DEFAULT_TIMEOUT,
    LOGGER,
    HaVersionChannel,
    HaVersionSource,
)
from .container import HaVersionContainer
from .exceptions import HaVersionFetchException, HaVersionParseException
from .haio import HaVersionHaio
from .local import HaVersionLocal
from .pypi import HaVersionPypi
from .supervisor import HaVersionSupervisor

_HANDLERS: dict[HaVersionSource, HaVersionBase] = {
    HaVersionSource.CONTAINER: HaVersionContainer,
    HaVersionSource.PYPI: HaVersionPypi,
    HaVersionSource.SUPERVISOR: HaVersionSupervisor,
    HaVersionSource.HAIO: HaVersionHaio,
    HaVersionSource.LOCAL: HaVersionLocal,
    HaVersionSource.DEFAULT: HaVersionLocal,
}


class HaVersion:
    """Haversion client class."""

    def __init__(
        self,
        session: ClientSession | None = None,
        source: HaVersionSource = HaVersionSource.DEFAULT,
        channel: HaVersionChannel = HaVersionChannel.DEFAULT,
        board: str = DEFAULT_BOARD,
        image: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Initialize the client."""
        self._handler: HaVersionBase = _HANDLERS[source](
            board=board,
            channel=channel,
            image=image,
            session=session,
            source=source,
            timeout=timeout,
        )

    @property
    def source(self) -> str:
        """Return the source."""
        return self._handler.source

    @property
    def etag(self) -> str | None:
        """Return the etag of the last request if any."""
        return self._handler.etag

    @property
    def version(self) -> AwesomeVersion | None:
        """Return the version."""
        return self._handler.version

    @property
    def version_data(self) -> dict[str, Any]:
        """Return extended version data for supported sources."""
        return self._handler.version_data

    async def get_version(
        self,
        *,
        etag: str | None = None,
    ) -> tuple[AwesomeVersion, dict[str, Any]]:
        """
        Get version update.

        Returns a tupe with version, version_data.
        """
        try:
            data = await self._handler.fetch(etag=etag)

        except asyncio.TimeoutError as exception:
            raise HaVersionFetchException(
                f"Timeout of {self._handler.timeout} seconds was "
                f"reached while fetching version for {self.source}"
            ) from exception

        except (ClientError, gaierror) as exception:
            raise HaVersionFetchException(
                f"Error fetching version information from {self.source} {exception}"
            ) from exception

        try:
            self._handler.parse(data)
        except (KeyError, TypeError, AttributeError) as exception:
            raise HaVersionParseException(
                f"Error parsing version information for {self.source} - {exception}"
            ) from exception

        LOGGER.debug("Version: %s", self.version)
        LOGGER.debug("Version data: %s", self.version_data)
        return self.version, self.version_data
