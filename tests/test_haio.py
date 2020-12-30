"""Tests for ha.io/version.json."""
from unittest.mock import patch
from tests.common import fixture
from pyhaversion.consts import HaVersionSource

import aiohttp
import pytest

from .const import (
    STABLE_VERSION,
)


@pytest.mark.asyncio
async def test_haio(HaVersion):
    """Test ha.io/version.json stable."""
    with patch(
        "pyhaversion.haio.HaVersionHaio.data",
        fixture("haio/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(session=session, source=HaVersionSource.HAIO)
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION
