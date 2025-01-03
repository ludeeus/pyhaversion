"""Fixtures for tests."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from pyhaversion import HaVersion as PyHaVersion

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


async def mocked_fetch(_: Any) -> None:
    """Mocked fetch."""


@pytest.fixture
def HaVersion() -> Generator[Any, Any, Any]:
    """Fixture."""
    with (
        patch(
            "pyhaversion.container.HaVersionContainer.fetch",
            return_value=mocked_fetch,
        ),
        patch("pyhaversion.haio.HaVersionHaio.fetch", return_value=mocked_fetch),
        patch("pyhaversion.local.HaVersionLocal.fetch", return_value=mocked_fetch),
        patch("pyhaversion.pypi.HaVersionPypi.fetch", return_value=mocked_fetch),
        patch(
            "pyhaversion.supervisor.HaVersionSupervisor.fetch",
            return_value=mocked_fetch,
        ),
    ):
        yield PyHaVersion
