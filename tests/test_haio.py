"""Tests for ha.io/version.json."""
import aiohttp
import pytest

from pyhaversion import HaVersion
from pyhaversion.consts import HaVersionSource
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_haio(aresponses):
    """Test ha.io/version.json stable."""
    aresponses.add(
        "www.home-assistant.io",
        "/version.json",
        "get",
        aresponses.Response(
            text=fixture("haio/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(session=session, source=HaVersionSource.HAIO)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION
