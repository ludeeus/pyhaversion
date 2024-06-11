"""HaVersionLocal class."""

from __future__ import annotations

from dataclasses import dataclass

from .base import HaVersionBase

try:
    from homeassistant.const import __version__ as localversion
except (ModuleNotFoundError, ImportError):
    localversion = None


@dataclass
class HaVersionLocal(HaVersionBase):
    """HaVersionLocal class."""

    def __post_init__(self):
        self._version = localversion
        super().__post_init__()

    def validate_input(self) -> None:
        """Raise HaVersionInputException if expected input are missing."""

    @property
    def version_data(self) -> None:
        """Return extended version data."""
        return {}
