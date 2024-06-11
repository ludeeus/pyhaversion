"""HaVersionLocal class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import HaVersionBase

try:
    from homeassistant.const import __version__ as localversion
except (ModuleNotFoundError, ImportError):
    localversion = None


@dataclass
class HaVersionLocal(HaVersionBase):
    """HaVersionLocal class."""

    def __post_init__(self) -> None:
        """Initialize the local version."""
        self._version = localversion
        self._version_data = {}
        super().__post_init__()

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""

    async def fetch(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[empty-body]
        """Logic to fetch new version data."""

    def parse(self, data: dict[str, Any]) -> None:
        """Logic to parse new version data."""
