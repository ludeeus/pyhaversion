"""Example usage of pyhaversion."""
import asyncio
import aiohttp
from pyhaversion import Version


async def test():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        data = Version(LOOP, branch="beta", session=session, image="default")
        await data.get_hassio_version()

        print("Version:", data.version)
        print("Attributes:", data.version_data)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
