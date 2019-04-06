"""Tests for pypi version."""
import asyncio
import aiohttp
import pytest
from pyhaversion import Version


@pytest.mark.asyncio
async def test_pypi():
    """Test pypi."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(asyncio.get_event_loop(), session=session)
        await haversion.get_pypi_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_pypi_beta():
    """Test pypi."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), branch='beta', session=session)
        await haversion.get_pypi_version()
        print(haversion.version)
        print(haversion.version_data)
