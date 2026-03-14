"""CLI routes for Authorization."""

from __future__ import annotations

import cyclopts

from ._config import get_config

commands = cyclopts.App(name="auth")

_BLANK_VALUE = ""


@commands.command
def save(token: str) -> int:
    """
    Save a TrackBear API token.

    This will be used for all other commands unless overwritten.

    Args:
        token (str): A TrackBear API token.

    Returns:
        int: Value of exit code
    """
    if _save(token):
        print(f"Saved the new token ***{token[-4:]}")
        return 0

    print("Failed to save token.")
    return 1


def _save(token: str) -> bool:
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

    except (ValueError, OSError):
        return False

    return True


@commands.command
def clear() -> int:
    """
    Clear the stored TrackBear API token.

    Returns:
        int: Value of exit code
    """
    if _clear():
        print("The token has been cleared.")
        return 0

    print("Unable to clear token.")
    return 1


def _clear() -> bool:
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

    except (ValueError, OSError):
        return False

    return True
