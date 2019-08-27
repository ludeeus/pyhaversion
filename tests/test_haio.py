"""Tests for PyPi."""

import json

import aiohttp
import pytest
from pyhaversion import HaIoVersion
from .const import (
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
)
from .fixtures.fixture_haio import haio_response


@pytest.mark.asyncio
async def test_haio(aresponses, event_loop, haio_response):
    """Test pypi stable."""
    aresponses.add(
        "www.home-assistant.io",
        "/version.json",
        "get",
        aresponses.Response(
            text=json.dumps(haio_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        haversion = HaIoVersion(event_loop, session)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION
