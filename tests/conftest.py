import logging
from unittest.mock import patch

import pytest

from pyhaversion import HaVersion as PyHaVersion

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


async def mocked_fetch(self):
    pass


@pytest.fixture
def HaVersion():
    with (
        patch("pyhaversion.container.HaVersionContainer.fetch", return_value=mocked_fetch),
        patch("pyhaversion.haio.HaVersionHaio.fetch", return_value=mocked_fetch),
        patch("pyhaversion.local.HaVersionLocal.fetch", return_value=mocked_fetch),
        patch("pyhaversion.pypi.HaVersionPypi.fetch", return_value=mocked_fetch),
        patch(
            "pyhaversion.supervisor.HaVersionSupervisor.fetch",
            return_value=mocked_fetch,
        ),
    ):
        yield PyHaVersion
