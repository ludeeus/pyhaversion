"""Fixtures."""
import pytest


@pytest.fixture()
def docker_response():
    """Response when no active beta."""
    return {
        "results": [
            {"name": "dev"},
            {"name": "9.99.9"},
            {"name": "latest"},
            {"name": "rc"},
            {"name": "beta"},
            {"name": "9.99.9b0"},
            {"name": "9.98.9"},
            {"name": "9.98.9b0"},
            {"name": "9.97.9"},
            {"name": "9.97.9b0"},
        ]
    }


@pytest.fixture()
def docker_response_beta_week():
    """Response when active beta."""
    return {
        "results": [
            {"name": "dev"},
            {"name": "beta"},
            {"name": "9.99.9b0"},
            {"name": "rc"},
            {"name": "latest"},
            {"name": "9.98.9"},
            {"name": "9.98.9b0"},
            {"name": "9.97.9"},
            {"name": "9.97.9b0"},
        ]
    }
