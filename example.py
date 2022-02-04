"""Example usage of pyhaversion."""
import asyncio

import aiohttp

from pyhaversion import HaVersion
from pyhaversion.consts import HaVersionChannel, HaVersionSource


async def example():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        sources = [
            HaVersionSource.CONTAINER,
            HaVersionSource.SUPERVISOR,
            HaVersionSource.HAIO,
            HaVersionSource.PYPI,
        ]
        for source in sources:
            version, data = await HaVersion(
                session=session,
                source=source,
                board="generic-x86-64",
                channel=HaVersionChannel.DEFAULT,
            ).get_version()
            print(source)
            print("Version:", version)
            print("Version data:", data)
            print()


async def example2():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        version, data = await HaVersion(
            session=session,
            source=HaVersionSource.SUPERVISOR,
            board="generic-x86-64",
            channel=HaVersionChannel.DEFAULT,
        ).get_version(etag='W/"bef52c6ed40179bdb6e844b9b7a88b67"')
        print(version)
        print(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(example2())
