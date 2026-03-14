"""CLI routes for Authorization."""

from __future__ import annotations

import cyclopts

from ._config import get_config

commands = cyclopts.App(name="auth")


@commands.command
def save(token: str) -> None:
    """
    Save a TrackBear API token.

    This will be used for all other commands unless overwritten.

    Args:
        token (str): A TrackBear API token.

    Returns:
        None
    """
    config = get_config()
    # TODO: This should eventually know if state has changed and noop whenever possible
    config.load()
    config.auth_token = token
    config.save()

    print(f"Saved the new token ***{config.auth_token[-4:]}")


@commands.command
def clear() -> None:
    """
    Clear the stored TrackBear API token

    Returns:
        None
    """
    config = get_config()
    config.load()
    config.auth_token = ""
    config.save()

    print("The TrackBear API token has been cleared.")
