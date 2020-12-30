"""Tests for ha.io/version.json."""
from pyhaversion import HaVersion
from unittest.mock import patch
from pyhaversion.consts import HaVersionSource

import aiohttp
import pytest

from .const import (
    STABLE_VERSION,
)


@pytest.mark.asyncio
async def test_local():
    """Test ha.io/version.json stable."""
    with patch(
        "homeassistant.const.__version__",
        STABLE_VERSION,
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.LOCAL)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION
