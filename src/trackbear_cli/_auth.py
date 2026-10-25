"""Authorization command implementation."""

from __future__ import annotations

from ._config import get_config

_BLANK_VALUE = ""


def save(token: str) -> bool:
    """
    Save a token to the config file. Handles reporting errors.

    Args:
        token (str): A TrackBear API token.

    Returns:
        bool: True if successful, otherwise False
    """
    config = get_config()
    try:
        config.load()
        config.auth_token = token
        config.save()

    except ValueError, OSError:
        return False

    return True


def clear() -> bool:
    """
    Clear the stored TrackBear API token.

    Returns:
        bool: True if successful, otherwise False.
    """
    config = get_config()

    try:
        config.load()
        config.auth_token = _BLANK_VALUE
        config.save()

    except ValueError, OSError:
        return False

    return True
