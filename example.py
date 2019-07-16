"""Example usage of pyhaversion."""
import asyncio
import aiohttp
from pyhaversion import DockerVersion


async def test():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        data = DockerVersion(LOOP, branch="beta", session=session, image="qemux86-64")
        await data.get_version()

        print("Version:", data.version)
        print("Attributes:", data.version_data)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
