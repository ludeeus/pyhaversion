"""Exceptions for pyhaversion."""


class HaVersionException(Exception):
    """Base pyhaversion exception."""


class HaVersionInputException(HaVersionException):
    """Raised when missing required input."""


class HaVersionFetchException(HaVersionException):
    """Raised there are issues fetching information."""


class HaVersionParseException(HaVersionException):
    """Raised there are issues parsing information."""
