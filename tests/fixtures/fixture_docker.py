"""Fixtures."""
import pytest


@pytest.fixture()
def docker_response():
    """Response when no active beta."""
    return {
        "results": [
            {"name": "dev"},
            {"name": "0.99.0.dev19700101"},
            {"name": "stable"},
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
            {"name": "0.99.0.dev19700101"},
            {"name": "stable"},
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


@pytest.fixture()
def docker_response_page1():
    """Response when no active beta."""
    return {
        "next": "https://registry.hub.docker.com/v2/repositories/homeassistant/home-assistant/tags/page2",
        "results": [
            {"name": "dev"},
            {"name": "latest"},
            {"name": "rc"},
            {"name": "beta"},
        ],
    }


@pytest.fixture()
def docker_response_beta_week_page1():
    """Response when active beta."""
    return {
        "next": "https://registry.hub.docker.com/v2/repositories/homeassistant/home-assistant/tags/page2",
        "results": [{"name": "dev"}, {"name": "rc"}, {"name": "latest"}],
    }


@pytest.fixture()
def docker_response_page2():
    """Response when no active beta."""
    return {
        "results": [
            {"name": "dev"},
            {"name": "latest"},
            {"name": "rc"},
            {"name": "beta"},
            {"name": "9.99.9"},
            {"name": "9.99.9b0"},
            {"name": "9.98.9"},
            {"name": "9.98.9b0"},
        ]
    }


@pytest.fixture()
def docker_response_beta_week_page2():
    """Response when active beta."""
    return {
        "results": [
            {"name": "dev"},
            {"name": "rc"},
            {"name": "latest"},
            {"name": "9.99.9b0"},
            {"name": "9.98.9"},
            {"name": "9.98.9b0"},
            {"name": "9.97.9"},
            {"name": "9.97.9b0"},
        ]
    }
