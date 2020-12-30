"""Tests for Hassio."""
from unittest.mock import patch
from tests.common import fixture
from pyhaversion.consts import HaVersionChannel, HaVersionSource

import aiohttp
import pytest

from .const import (
    BETA_VERSION,
    STABLE_VERSION,
)


@pytest.mark.asyncio
async def test_stable_version(HaVersion):
    """Test hassio stable."""
    with patch(
        "pyhaversion.supervised.HaVersionSupervised.data",
        fixture("supervised/default"),
    ):
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
