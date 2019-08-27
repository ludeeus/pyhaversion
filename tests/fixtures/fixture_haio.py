"""Fixtures."""
import pytest


@pytest.fixture()
def haio_response():
    """Response for https://www.home-assistant.io/version.json."""
    return {"current_version": "9.99.9"}
