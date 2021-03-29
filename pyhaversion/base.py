import aiohttp
from awesomeversion import AwesomeVersion

from .consts import (
    DATA_CHANNEL,
    DATA_SOURCE,
    DEFAULT_BOARD,
    DEFAULT_TIMEOUT,
    HaVersionChannel,
    HaVersionSource,
)


class HaVersionBase:
    def __init__(
        self,
        session: aiohttp.ClientSession = None,
        source: HaVersionSource = HaVersionSource.DEFAULT,
        channel: HaVersionChannel = HaVersionChannel.DEFAULT,
        board: str = DEFAULT_BOARD,
        timeout: int = DEFAULT_TIMEOUT,
        image: str = None,
    ) -> None:
        self.session = session
        self.source = source
        self.channel = channel
        self.board = board
        self.image = image
        self.timeout = timeout

        self._data = {}
        self._version = None
        self._version_data = {}

        self.validate_input()

    @property
    def data(self) -> dict:
        """Return the version."""
        return self._data

    @property
    def version(self) -> AwesomeVersion:
        """Return the version."""
        return AwesomeVersion(self._version) if self._version else None

    @property
    def version_data(self) -> dict:
        """Return extended version data for supported sources."""
        if not self._version_data:
            self._version_data = {}
        self._version_data[DATA_SOURCE] = self.source
        self._version_data[DATA_CHANNEL] = self.channel
        return self._version_data

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""

    async def fetch(self):
        """Logic to fetch new version data."""

    def parse(self):
        """Logic to parse new version data."""
