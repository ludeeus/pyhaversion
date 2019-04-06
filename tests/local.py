"""Tests for local version."""
import asyncio
import aiohttp
import pytest
from pyhaversion import Version


@pytest.mark.asyncio
async def test_local():
    """Test local."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(asyncio.get_event_loop(), session=session)
        await haversion.get_local_version()
        print(haversion.version)
        print(haversion.version_data)
