"""Tests for Hassio."""
from unittest.mock import patch

import aiohttp
import pytest

from pyhaversion import HaVersion
from pyhaversion.consts import HaVersionChannel, HaVersionSource
from pyhaversion.exceptions import HaVersionInputException
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_stable_version(aresponses):
    """Test hassio stable."""
    aresponses.add(
        "version.home-assistant.io",
        "/stable.json",
        "get",
        aresponses.Response(
            text=fixture("supervised/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        haversion = HaVersion(session=session, source=HaVersionSource.SUPERVISED)
        await haversion.get_version()
        assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(HaVersion):
    """Test hassio beta."""
    with patch(
        "pyhaversion.supervised.HaVersionSupervised.data",
        fixture("supervised/default"),
    ):
        async with aiohttp.ClientSession() as session:
            haversion = HaVersion(
                session=session,
                source=HaVersionSource.SUPERVISED,
                channel=HaVersionChannel.BETA,
            )
            await haversion.get_version()
            assert haversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_input_exception(HaVersion):
    with pytest.raises(HaVersionInputException):
        HaVersion(source=HaVersionSource.SUPERVISED)
