"""Tests for hassio version."""
import asyncio
import aiohttp
import pytest
from pyhaversion import Version


@pytest.mark.asyncio
async def test_hassio():
    """Test hassio."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(asyncio.get_event_loop(), session=session)
        await haversion.get_hassio_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_hassio_beta():
    """Test hassio."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(asyncio.get_event_loop(), branch='beta',
        session=session)
        await haversion.get_hassio_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_hassio_valid_image():
    """Test hassio."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), image='raspberrypi3',
            session=session)
        await haversion.get_hassio_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_hassio_not_valid_image():
    """Test hassio."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), image='not_valid', session=session)
        await haversion.get_hassio_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_hassio_valid_image_beta():
    """Test hassio."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), branch='beta', image='raspberrypi3',
            session=session)
        await haversion.get_hassio_version()
        print(haversion.version)
        print(haversion.version_data)


@pytest.mark.asyncio
async def test_hassio_not_valid_image_beta():  # pylint: disable=invalid-name
    """Test hassio."""
    async with aiohttp.ClientSession() as session:
        haversion = Version(
            asyncio.get_event_loop(), branch='beta', image='not_valid',
            session=session)
        await haversion.get_hassio_version()
        print(haversion.version)
        print(haversion.version_data)
