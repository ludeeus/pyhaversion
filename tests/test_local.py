"""Tests for ha.io/version.json."""
from unittest.mock import MagicMock, patch

import aiohttp
import pytest

from pyhaversion import HaVersion
from pyhaversion.consts import HaVersionSource

from .const import STABLE_VERSION


@pytest.mark.asyncio
async def test_local():
    """Test ha.io/version.json stable."""
    with patch.dict(
        "sys.modules", {"homeassistant.const": MagicMock(__version__=STABLE_VERSION)}
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.LOCAL)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION
