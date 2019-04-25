"""Fixtures."""
import pytest


@pytest.fixture()
def hassio_response():
    """Response when no active beta"""
    return {
        "supervisor": "999",
        "homeassistant": {"default": "9.99.9"},
        "hassos": {"ova": "9.99"},
        "hassos-cli": "9",
    }


@pytest.fixture()
def hassio_beta_response():
    """Beta response when no beta during beta week."""
    return {
        "supervisor": "999",
        "homeassistant": {"default": "9.99.9"},
        "hassos": {"ova": "9.99"},
        "hassos-cli": "9",
    }


@pytest.fixture()
def hassio_response_beta_week():
    """Response when active beta during beta week."""
    return {
        "supervisor": "999",
        "homeassistant": {"default": "9.98.9"},
        "hassos": {"ova": "9.99"},
        "hassos-cli": "9",
    }


@pytest.fixture()
def hassio_beta_response_beta_week():
    """Beta response when active beta during beta week."""
    return {
        "supervisor": "999",
        "homeassistant": {"default": "9.99.9b0"},
        "hassos": {"ova": "9.99"},
        "hassos-cli": "9",
    }
